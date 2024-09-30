import pandas as pd
from deep_translator import GoogleTranslator as GT
from tqdm import tqdm

# Load the CSV file
df = pd.read_csv('data.csv')

# Initialize Google Translator (For example, English to Spainish)
translator_en_es = GT(source='en', target='es')
tqdm.pandas()

# Translate
df['Spain'] = df['English'].progress_apply(lambda x: translator_en_es.translate(x))

# Save the translated DataFrame to a new CSV file
df.to_csv('data_translated.csv', index=False)

for language, code in supported_languages.items():
    print(f"Language: {language}, Code: {code}")
