import csv
import requests
from bs4 import BeautifulSoup as BS



HOST = 'https://www.kivano.kg/'

def get_html(url):
    response = requests.get(url)
    return(response.text)

def get_total_pages(html):
    soup = BS(html, 'lxml')
    pages_ul = soup.find('div', class_= "pager-wrap").find('ul')
    last_page = pages_ul.find_all('li') [-1]
    total_page = last_page.find('a').get('href').split('=')[-1]
    return int(total_page)

def write_to_csv(data):
    with open('kivano_notebooks.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'], 
                         data['price'],
                         data['photo']))

def get_page_data(html):
    soup = BS(html, 'lxml')
    product_list = soup.find('div', class_="list-view")
    products = product_list.find_all('div', class_="item product_listbox oh")

    for product in products:
        try:
            
            photo = HOST + product.find('div', class_="listbox_img pull-left").find('a').find('img').get('src')

        except:
            photo = ''

        try:
            title = product.find('div', class_='listbox_title oh').find('a').text
            
        except:
            title = ''
        try:
            price = product.find('div', class_='listbox_price text-center').find('strong').text
            
        except:
            price = ''

        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)


def main():
    notebook_url = 'https://www.kivano.kg/noutbuki'
    pages = '?page='
    
    total_pages = get_total_pages(get_html(notebook_url))
    
    for page in range(1, total_pages+1):
        url_with_page = notebook_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)



main()    

