import pandas as pd
import configparser
import nltk
import re
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords


# Configuration items
config = configparser.RawConfigParser()
config.optionxform = lambda option: option
config.read('/Users/divinefavourodion/Documents/TLNP_Project/config.ini')
data_path = dict(config.items('data'))['training_data']

# load the CSV file into a pandas dataframe
df = pd.read_csv(data_path)

# Define a function to remove stopwords from a given text
def remove_stopwords(text):
    # tokenize the text into individual words
    words = nltk.word_tokenize(str(text))
    # remove stopwords from the text
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
    # re-join the filtered words into a single string
    filtered_text = ' '.join(filtered_words)
    return filtered_text

# Define a function to remove punctuation, large indentation blocks, and convert all text to lowercase
def clean_text(text):
    # remove punctuation from the text
    text = re.sub(r'[^\w\s]', '', text)
    # remove large indentation blocks
    text = re.sub(r'\n\s*\n', '\n', text)
    # convert all text to lowercase
    text = text.lower()
    return text


# Apply the remove_stopwords function to the 'content' column of the dataframe
df['content'] = df['content'].apply(remove_stopwords)

# Apply the clean_text function to the 'content' column of the dataframe
df['content'] = df['content'].apply(clean_text)

print('...')

# save the modified dataframe to a new CSV file
#df.to_csv('articles_without_stopwords.csv', index=False)
