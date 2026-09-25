import pandas as pd
import json
import re
import os

def audit_hospital_invoices(hospital_id, invoices_path, line_items_path, contract_rules_path, mapping_path, submission_path='../submission.csv'):
    invoices_df = pd.read_csv(invoices_path)
    line_items_df = pd.read_csv(line_items_path)
    
    with open(contract_rules_path, 'r', encoding='utf-8') as f:
        contract_rules = json.load(f)
    with open(mapping_path, 'r', encoding='utf-8') as f:
        service_mapping = json.load(f)
        
    rules_dict = {item['service_name']: item for item in contract_rules['services']}
    
    expected_totals, error_cats, confidences = [], [], []
    for idx, row in line_items_df.iterrows():
        billed_desc = row['description']
        quantity = row['quantity']
        
        mapping_data = service_mapping.get(billed_desc, {})
        official_service = mapping_data.get('mapped_service')
        confidence = mapping_data.get('confidence_score', 0)
        
        if official_service and official_service in rules_dict and confidence >= 60:
            base_price = rules_dict[official_service]['unit_price_cents']
            expected_total = quantity * base_price
            error_cat = "Clean"
        else:
            expected_total = 0
            error_cat = "Unmapped Service"
            confidence = 0.0
            
        expected_totals.append(expected_total)
        error_cats.append(error_cat)
        confidences.append(confidence / 100.0)
        
    line_items_df['expected_line_total'] = expected_totals
    line_items_df['line_confidence'] = confidences
    
    invoice_summary = line_items_df.groupby('invoice_id').agg(
        expected_total_cents=('expected_line_total', 'sum'),
        min_confidence=('line_confidence', 'min')
    ).reset_index()
    
    final_audit_df = invoices_df.merge(invoice_summary, on='invoice_id', how='left')
    final_audit_df['expected_total_cents'] = final_audit_df['expected_total_cents'].fillna(0)
    final_audit_df['min_confidence'] = final_audit_df['min_confidence'].fillna(0.0)
    final_audit_df['flagged'] = (abs(final_audit_df['invoice_total_cents'] - final_audit_df['expected_total_cents']) > 2).astype(int)
    
    def categorize_error(row):
        if row['flagged'] == 0: return ""
        if row['min_confidence'] < 0.6: return "Low Confidence Mapping"
        if row['invoice_total_cents'] > row['expected_total_cents']: return "Overbilled"
        return "Underbilled"
        
    final_audit_df['error_category'] = final_audit_df.apply(categorize_error, axis=1)
    
    new_submission_df = pd.DataFrame({
        'invoice_id': final_audit_df['invoice_id'],
        'flagged': final_audit_df['flagged'],
        'error_category': final_audit_df['error_category'],
        'expected_total_cents': final_audit_df['expected_total_cents'].astype(int),
        'billed_total_cents': final_audit_df['invoice_total_cents'].astype(int),
        'confidence': final_audit_df['min_confidence'].round(2)
    })
    
    new_submission_df['hospital_temp'] = hospital_id
    if os.path.exists(submission_path):
        existing_df = pd.read_csv(submission_path)
        if 'hospital_temp' not in existing_df.columns:
            existing_df['hospital_temp'] = 'hospital_1'
        combined_df = pd.concat([existing_df, new_submission_df]).drop_duplicates(subset=['hospital_temp', 'invoice_id'], keep='last')
    else:
        combined_df = new_submission_df
        
    combined_df.drop(columns=['hospital_temp']).to_csv(submission_path, index=False)
    print(f"✅ تم تدقيق {hospital_id} وحفظ النتائج بنجاح في submission.csv")