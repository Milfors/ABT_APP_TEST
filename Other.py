import requests
from bs4 import BeautifulSoup

url = 'https://abt-professional.com/magazin/other-products/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='product-thumb')

OtherPrice = []

for n, i in enumerate(items, start=0):
    #itemName = i.find('h4', class_='name').text.strip()
    itemPrice = i.find('p', class_='price').text
    OtherPrice.append(itemPrice[1:-6].replace(' ', ''))
    #print(f'{n}: {itemPrice} за {itemName}')

#print(OtherPrice)


