import json
import csv

def load_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    # Remove "#: " from the values
    for row in data:
        for key in row:
            if row[key].startswith("#: "):
                row[key] = row[key][3:]  # Remove the first three characters
    return data

def generate_json(data, lang):
    """Generate JSON from CSV data."""
    json_data = {}
    for row in data:
        keys = row['Key'].split('.')
        current_level = json_data
        for key in keys[:-1]:
            current_level = current_level.setdefault(key, {})
        current_level[keys[-1]] = row[lang]
    return json_data

def save_json(data, file_path):
    """Save JSON to file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    csv_data = load_csv('translated_results_updated.csv')

    en_json = generate_json(csv_data, "English")
    save_json(en_json, 'en_updated.json')
    print("Updated English JSON saved to en_updated.json")

    es_json = generate_json(csv_data, "Spanish")
    save_json(es_json, 'es_updated.json')
    print("Updated Spanish JSON saved to es_updated.json")

if __name__ == "__main__":
    main()
