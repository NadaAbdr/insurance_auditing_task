import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def extract_contract_rules(contract_text, prompt_template, output_json_path):
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    
    response = model.generate_content(prompt_template + "\n\n" + contract_text)
    extracted_text = response.text.strip()
    
    if extracted_text.startswith("```json"):
        extracted_text = extracted_text[7:-3].strip()
    elif extracted_text.startswith("```"):
        extracted_text = extracted_text[3:-3].strip()
        
    contract_rules = json.loads(extracted_text)
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(contract_rules, f, indent=4)
    return contract_rules