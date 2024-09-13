import pandas as pd
from deep_translator import GoogleTranslator as GT
from tqdm import tqdm

# Load the CSV file
df = pd.read_csv('translated_results_updated.csv')

# Initialize Google Translator
translator_en_fr = GT(source='en', target='fr')
tqdm.pandas()

# Translate English column headers to Canadian French
df['French'] = df['English'].progress_apply(lambda x: translator_en_fr.translate(x))

# Save the translated DataFrame to a new CSV file
df.to_csv('translated_results_updated_with_french.csv', index=False)
