import requests
from bs4 import BeautifulSoup as bs
import csv

def writer_to_csv(data: dict):
    with open('mashina.csv', 'a') as file:
        write = csv.writer(file)
        write.writerow((data['name'],data['price'],data['img'],data['description']))


def get_html(url):
    response = requests.get(url)
    return response.text

def get_page(html):
    soup = bs(html,'lxml')
    pages = soup.find('ul', class_ = 'pagination').find_all('li')
    last_page = pages[-4].text
    return int(last_page)

def get_data(html):
    soup = bs(html, 'lxml')
    cars = soup.find_all('div', class_="list-item list-label")
    for car in cars:
        car_data = car.find('a')
        try:
            name = car_data.find('h2',class_="name").text.strip()
        except:
            name = ''
        # print(name)
        try:
            price = car_data.find('p').text.replace(' ','')
        except:
            price = ''
        # print(price)
        try:
            img = car.find('img').get('src')
        except:
            img = ''
        # print(img)
        try:
            description = car.find('div', class_="block info-wrapper item-info-wrapper").text.replace(' ','')
        except:
            description = ''
        # print(description)
        data = {'name': name,
                'price': price,
                'img': img,
                'description': description}
        writer_to_csv(data)


def main():
    url = 'https://www.mashina.kg/search/all/'
    html = get_html(url)
    get_data(html)
    num = get_page(html)
    i = 0
    while i <= num:
        for i in range(0, num+1): 
            url = f'https://www.mashina.kg/search/all/?page={i}'
            print(url)
        html = get_html(url)
        get_data(html)
        if i == num:
            num = int(get_page(html))
    i += 1
        


with open('mashina.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['name', 'price','img','description'])

main()
