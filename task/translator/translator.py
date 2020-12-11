import requests
import sys
import os

from bs4 import BeautifulSoup


# print("""Hello, you're welcome to the translator. Translator supports:
# 1. Arabic
# 2. German
# 3. English
# 4. Spanish
# 5. French
# 6. Hebrew
# 7. Japanese
# 8. Dutch
# 9. Polish
# 10. Portuguese
# 11. Romanian
# 12. Russian
# 13. Turkish""")

args = sys.argv
# user_language = int(input('Type the number of your language:\n'))
user_language = args[1]
# translator_language = int(input('Type the number of language you want to translate to:\n'))
translator_language = args[2]
# word = input('Type the word you want to translate:\n')
word = args[3]

switcher = {
        1: "arabic",
        2: "german",
        3: "english",
        4: "spanish",
        5: "french",
        6: "hebrew",
        7: "japanese",
        8: "dutch",
        9: "polish",
        10: "portuguese",
        11: "romanian",
        12: "russian",
        13: "turkish"
    }

file_name = f'{word}.txt'
my_file = open(file_name, 'w+', encoding='utf-8')
s = requests.Session()


def translator(link, translation_language):
    global my_file, word
    user_agent = 'Mozilla/5.0'

    r = s.get(link, headers={'User-Agent': user_agent})

    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup)

        word_container = soup.find(id="translations-content")
        # print(word_container)
        words = word_container.find_all('a')
        translated_word = [word.text.strip() for word in words]

        example_container = soup.find(id="examples-content")
        # print(example_container)
        examples = example_container.find_all('span', class_="text")
        # print(examples)
        sentences = [(example.text.strip()) for example in examples]

        if translator_language == 'all':
            # my_file.write(f'\n{switcher[translation_language].capitalize()} Translations:\n')
            my_file.write(f'\n{translation_language.capitalize()} Translations:\n')
            my_file.write(translated_word[0] + '\n')

            # my_file.write(f'\n{switcher[translation_language].capitalize()} Examples:\n')
            my_file.write(f'\n{translation_language.capitalize()} Examples:\n')

            my_file.write(f'{sentences[0]}:\n{sentences[1]}\n\n')
        else:
            my_file.write(f'\n{translation_language.capitalize()} Translations:\n')
            for i in range(5):
                my_file.write(translated_word[i] + '\n')

            # my_file.write(f'\n{switcher[translation_language].capitalize()} Examples:\n')
            my_file.write(f'\n{translation_language.capitalize()} Examples:\n')
            for i in range(5):
                my_file.write(f'{sentences[2*i]}:\n{sentences[2*i+1]}\n\n')


def main():
    global translator_language, my_file

    if translator_language == 'all':

        for i in range(len(switcher)):
            if switcher[i+1] != user_language:
                url = f'https://context.reverso.net/translation/{user_language}-{switcher[i+1]}/{word}'
                translator(url, switcher[i+1])
    else:
        url = f'https://context.reverso.net/translation/{user_language}-{translator_language}/{word}'
        translator(url, translator_language)

    my_file.seek(0)
    if os.path.getsize(file_name) != 0:
        print(my_file.read())
    else:
        print(f"Sorry, unable to find {word}")
    my_file.close()


try:
    main()
except ConnectionError:
    print("Something wrong with your internet connection")
except AttributeError:
    print(f"Sorry, the program doesn't support {translator_language}")

