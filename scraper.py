from bs4 import BeautifulSoup
import requests
import pandas as pd
from pathlib import Path

def scrape():

    link = 'https://quotes.toscrape.com/'

    webpage = requests.get(link)
    soup = BeautifulSoup(webpage.text, features = 'html.parser')

    tags = soup.css.select('.tag-item .tag')

    webpage_tags = {}

    for tag in tags:
        webpage_tags[tag.text] = link[:-1] + tag.get('href')

    quotes_dict = {
        'tag': [],
        'quote': [],
        'author': []
    }
        
    for text, tag in webpage_tags.items():
        
        sub_webpage = requests.get(tag)
        sub_soup = BeautifulSoup(sub_webpage.text, 'html.parser')
        
        quotes = sub_soup.css.select('.quote')
        
        for quote in quotes:
            quotes_dict['tag'].append(text)
            quotes_dict['quote'].append(quote.select_one('.text').text)
            quotes_dict['author'].append(quote.select_one('.author').text)
            
    df = pd.DataFrame(quotes_dict)
    
    return df

if __name__ == '__main__':
    
    try:
        PATH = str(input('Please input path to generate .csv file: '))
        NAME = str(input('Please input the desired name of the file: '))
        scrape().to_csv(Path(PATH, NAME + '.csv'))
        
    except:
        print('Unable to generate .csv file.')
        print('Please check the input path of the filename (file extension not needed)')