import requests
from bs4 import BeautifulSoup

url = 'https://abt-professional.com/index.php?route=product/category&path=60_69'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='product-thumb')

Pedicure_discs = []

for n, i in enumerate(items, start=0):
    #itemName = i.find('h4', class_='name').text.strip()
    itemPrice = i.find('p', class_='price').text
    Pedicure_discs.append(itemPrice[1:-6].replace(' ', ''))
    #print(f'{n}: {itemPrice} за {itemName}')

#print(Pedicure_discs)