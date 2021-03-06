import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests as req
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Read names script')
parser.add_argument('-out', action="store", dest="file_out_name", default='bessmertnybarak.csv', type=str, required=True)
parser.add_argument('-href', action="store", dest="href_to_parse", default='https://bessmertnybarak.ru', type=str)
args = parser.parse_args()


hrefs = []
names = []
start_href = args.href_to_parse
fileout_name = args.file_out_name

if start_href != 'https://bessmertnybarak.ru':
	print ('Sorry href is unsupported')

# итерация по страницам сайта, их всего 137
# затем обираем ссылки и имена людей, помещаем их в массив:
for page in tqdm(range(1, 137)):
    href = 'https://bessmertnybarak.ru/books/vozv_imena/page-{0}/'.format(page)
    resp = req.get(href)
    soup = BeautifulSoup(resp.text, 'lxml')
    people = soup.find_all(class_='personName')
    for i in range(len(people)):
        hrefs.append(start_href + people[i].find('a').get('href'))
        names.append(people[i].find('p').get_text())

# узнаю длину ссылки, она всегда одинаковая и = 47
len(hrefs[0])

# проверяю, что у каждого есть веб страница
for i in range(len(hrefs)):
    if len(hrefs[i]) != 47:
        print('Error', i, hrefs[i])
# есть у каждого

# создаем дата фрейм
column = np.asarray([names, hrefs]).T
data = pd.DataFrame(column, columns=['Имя', 'Ссылка(гипер)'])
# пишем в файл
data.to_csv(fileout_name, index=False)
