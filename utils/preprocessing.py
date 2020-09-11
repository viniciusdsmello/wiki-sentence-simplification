import unicodedata
import re
from bs4 import BeautifulSoup


def remove_html_tags(text):
    return BeautifulSoup(text, 'html.parser').get_text()

def remove_accented_chars(text):
    new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text

# function to remove special characters
def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\'\"\`\s]' 
    return re.sub(pat, '', text)

def remove_extra_whitespace_tabs(text):
    pattern = r'^\s*|\s\s*'
    return re.sub(pattern, ' ', text).strip()

def replace_quotes(text):
    pattern = r'(["\'`]){2,}'
    return re.sub(pattern, '\"', text).strip()

def to_lowercase(text):
    return text.lower()

def preprocessing(x: str):
    x = remove_accented_chars(x)
    x = remove_special_characters(x)
    x = remove_extra_whitespace_tabs(x)
    x = replace_quotes(x)
    x = to_lowercase(x)
    x = x.strip()
    return x

if __name__ == "__main__":
    text = "eddie hazel is listed at 43 in rolling stone magazine 's `` 100 greatest guitarists of all time '' issue ."
    print(preprocessing(text))