from deep_translator import GoogleTranslator as GT

translator = GT()
supported_languages = translator.get_supported_languages(as_dict=True)

for language, code in supported_languages.items():
    print(f"Language: {language}, Code: {code}")