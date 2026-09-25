import pandas as pd
import json
import os
from rapidfuzz import process, fuzz

def map_invoice_items(line_items_path, contract_rules_path, output_mapping_path):
    line_items_df = pd.read_csv(line_items_path)
    with open(contract_rules_path, 'r', encoding='utf-8') as f:
        contract_rules = json.load(f)
        
    official_services = [s['service_name'] for s in contract_rules['services']]
    billed_descriptions = line_items_df['description'].unique()
    
    mapping_dict = {}
    for billed_desc in billed_descriptions:
        clean_desc = billed_desc.split('/')[0].strip() if '/' in billed_desc else billed_desc
        best_match = process.extractOne(clean_desc, official_services, scorer=fuzz.token_sort_ratio)
        
        if best_match:
            matched_service, score, _ = best_match
            mapping_dict[billed_desc] = {
                "mapped_service": matched_service,
                "confidence_score": round(score, 2)
            }
            
    os.makedirs(os.path.dirname(output_mapping_path), exist_ok=True)
    with open(output_mapping_path, 'w', encoding='utf-8') as f:
        json.dump(mapping_dict, f, indent=4)
    return mapping_dict