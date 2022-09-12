import requests
from bs4 import BeautifulSoup
import re

import csv
  
import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()

cur.execute("CREATE TABLE data(id integer primary key, url, headline,author,published)")


r=requests.get('https://www.theverge.com/')

soup = BeautifulSoup(r.text, 'html.parser')

a=[]

c=[]

for i in soup.find_all('a',href=True):
    if(re.search('data-analytics-link="article"',str(i))):
        a.append(i['href'])
        #print(a['href'])
    

for j in a:
    b={}
    r=requests.get(j)
    soup = BeautifulSoup(r.text, 'html.parser')
    b['id']=a.index(j)+1
    b['url']=j
    b['title']=soup.find("h1").getText()
    
    b['author']=[a for a in soup.find_all('span') if(re.search('class="c-byline__author-name"',str(a)))][-1].getText()
    b['posted_on']=soup.find('time').getText().split('\n')[1].strip()
    print(b['posted_on'],b['title'])
    c.append(list(b.values()))



# field names 
fields = ['id', 'Url', 'Headline', 'Author','Date'] 
    

  
with open('data.csv', 'w',newline='') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(c)

for data in c:
    cur.execute("INSERT INTO data(id, url, headline,author,published) VALUES(?, ?, ?, ?, ?)",(data[0],
    data[1], data[2],data[3],data[4]))
    
con.commit()


print(c)