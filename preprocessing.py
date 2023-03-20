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

# Function to create bigram features
def get_bigrams(text):
    bigram_list = [] # List to store the indexes of the max frequency bi-grams
    max_bigrams = [] # List to store the bigram strings
    txt = text.split(" ")
    bigram_count = (pd.Series(nltk.ngrams(txt, 2)).value_counts()) # Return the frequency count of all bigrams in the text

    if bigram_count.empty:
        return " "
    else:
        bigram_list.append(bigram_count[bigram_count > (max(bigram_count) - 2)].index)

        for i in range(len(bigram_list)):
            max_bigrams.append(list(bigram_list[i][0]))

        return max_bigrams



# Function to create trigram features
def get_trigrams(text):
    trigram_list = [] # List to store the indexes of the max frequency bi-grams
    max_trigrams = [] # List to store the bigram strings
    txt = text.split(" ")
    trigram_count = (pd.Series(nltk.ngrams(txt, 3)).value_counts()) # Return the frequency count of all bigrams in the text

    if trigram_count.empty:
        return " "
    else:
        trigram_list.append(trigram_count[trigram_count > (max(trigram_count) - 3)].index)

        for i in range(len(trigram_list)):
            max_trigrams.append(list(trigram_list[i][0]))

        return max_trigrams



# Apply the remove_stopwords function to the 'content' column of the dataframe
df['content'] = df['content'].apply(remove_stopwords)

# Apply the clean_text function to the 'content' column of the dataframe
df['content'] = df['content'].apply(clean_text)

# Apply the trigram function to the 'content' column of the dataframe
df['bi_grams'] = df['content'].apply(get_bigrams)

# Apply the trigram function to the 'content' column of the dataframe
df['tri_grams'] = df['content'].apply(get_trigrams)


# save the modified dataframe to a new CSV file
df.to_csv('articles_without_stopwords.csv', index=False)
