import json
import csv
from tqdm import tqdm
from deep_translator import GoogleTranslator as GT

def load(file_path, encoding='utf-8'):
    """Load JSON file."""
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

def compare_keys(json1, json2, prefix='', results=None, swap=False):
    """Compare keys between two JSON objects."""
    if results is None:
        results = []

    for key in json1:
        full_key = f"{prefix}.{key}" if prefix else key
        if key not in json2:
            if isinstance(json1[key], dict):
                sub_results = compare_keys(json1[key], {}, prefix=full_key, swap=swap)
                results.extend(sub_results)
            else:
                if swap:
                    results.append((full_key, '', json1[key]))  
                else:
                    results.append((full_key, json1[key], ''))  
        else:
            if isinstance(json1[key], dict) and isinstance(json2[key], dict):
                sub_results = compare_keys(json1[key], json2[key], prefix=full_key, swap=swap)
                results.extend(sub_results)
            else:
                if swap:
                    results.append((full_key, json2[key], json1[key]))  
                else:
                    results.append((full_key, json1[key], json2[key]))  

    return results

def filter_duplicates(en_results, es_results):
    """Filter duplicate keys."""
    en_keys = set(key for key, _, _ in en_results)
    return [(key, en_val, es_val) for key, en_val, es_val in es_results if key not in en_keys]

def save_to_csv(results, file_path):
    """Save results to a CSV file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'en value', 'es value'])
        writer.writerows(results)

def insert_es_into_en(en_results, es_results_filtered):
    """Insert Spanish results into English results."""
    for es_key, es_en_val, es_es_val in es_results_filtered:
        parent_key = es_key.rsplit('.', 1)[0]  
        for index, (en_key, _, _) in enumerate(en_results):
            if parent_key == en_key.rsplit('.', 1)[0]:  
                en_results.insert(index + 1, (es_key, es_en_val, es_es_val))  
                break
        else:
            en_results.append((es_key, es_en_val, es_es_val))  
    return en_results

def translate_missing(results):
    """Translate missing values."""
    translated_results = []
    translator_en_es = GT(source='en', target='es')
    translator_es_en = GT(source='es', target='en')
    
    for key, en_val, es_val in tqdm(results):
        if not en_val:
            translated_en_val = "#: " + translator_es_en.translate(es_val)
            translated_results.append((key, translated_en_val, es_val))
        elif not es_val:
            translated_es_val = "#: " + translator_en_es.translate(en_val)
            translated_results.append((key, en_val, translated_es_val))
        else:
            translated_results.append((key, en_val, es_val))
    return translated_results

def main():
    en_json = load('en.json')
    es_json = load('es.json')

    en_results = compare_keys(en_json, es_json)
    es_results = compare_keys(es_json, en_json, swap=True)

    es_results_filtered = filter_duplicates(en_results, es_results)

    combined_results = insert_es_into_en(en_results, es_results_filtered)

    save_to_csv(combined_results, 'combined_results.csv')
    print("Comparison completed. Results saved to combined_results.csv")

    translated_results = translate_missing(combined_results)

    save_to_csv(translated_results, 'translated_results.csv')
    print("Translation completed. Results saved to translated_results.csv")

if __name__ == "__main__":
    main()
