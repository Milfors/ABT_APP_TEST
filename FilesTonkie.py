import requests
from bs4 import BeautifulSoup

url = 'https://abt-professional.com/magazin/faili-na-osnovi-pilki/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='product-thumb')

Removable_files_on_a_thin_basis = []

for n, i in enumerate(items, start=0):
    #itemName = i.find('h4', class_='name').text.strip()
    itemPrice = i.find('p', class_='price').text
    Removable_files_on_a_thin_basis.append(itemPrice[1:-6].replace(' ', ''))
    #print(f'{n}: {itemPrice} за {itemName}')

#print(Removable_files_on_a_thin_basis)


