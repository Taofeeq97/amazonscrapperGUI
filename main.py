import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import csv
from csv import writer


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/2010010 Firefox/94.0',
    'Accept-Language':'en-US, en;q=0.5'
}
search_query=input("please kindly input the name of the products you want to scrape off amazon: ")
search_querys= search_query.replace(' ', '+')
base_url='https://www.amazon.com/s?k={0}'.format(search_query)
items=[]
for i in range(1,4):
    print('Processing {0}.....'.format(base_url+'&page={0}'.format(i)))
    response=requests.get(base_url+ '&page={0}'.format(i), headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    results=soup.find_all('div', class_='s-result-item')


    product_names=[product_name.getText() for product_name in soup.find_all('span', class_='a-size-base-plus')]

    try:
        ratings = [rating.getText() for rating in soup.find_all('i', class_='a-icon')]
        rating_counts=[rating_count.getText() for rating_count in soup.find_all('span', class_='a-size-base', id='acrCustomerReviewText')]
    except AttributeError:
        continue

    try:
        price = [price1.getText() for price1 in soup.find_all('span', class_='a-price-whole')]
        product_websites = ['https://www.amazon.com' + product_website.get("href") for product_website in
                        soup.find_all('a', class_='a-link-normal s-link-style a-text-normal')]
        item=product_names+ratings+rating_counts+price+product_websites
        items.append(item)
        file = open("{0}.csv".format(search_query), "w")
        writer = csv.writer(file)
        header = ['Product name', 'ratings', 'rating counts', 'price', "Product links"]
        writer.writerow(header)

        for details in range(60):
            writer.writerow([product_names[details], ratings[details], rating_counts[details], price[details],
                         product_websites[details]])




    except AttributeError:
        continue


