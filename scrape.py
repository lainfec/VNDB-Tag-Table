from bs4 import BeautifulSoup
import requests
import re
import csv

vn_list=[]
tag_dict={}

usr_num=input("Enter your vndb user number. If its u100, enter 100.\n")

print("Getting a list of all Vns. Please wait.")

pg_num=0
while 1:
    url='https://vndb.org/u{}/ulist?mul=1&o=a&p={}&s=title'.format(usr_num,pg_num+1)
    r=requests.get(url)
    data=r.text
    soup=BeautifulSoup(data, 'html5lib')
    temp_list=[]
    flag=0
    for link in soup.find_all('a'):
        if link.get('href')[:2]=='/v':
            temp_list+=[link.get('href')]
        if link.get('href')[:13]=="?mul=1&o=a&p=":
            if link.get_text()[:4]=="next":
                flag=1
    vn_list.extend(temp_list[2:-1])
    print("Page ", pg_num+1, " complete.")
    if flag==1:
      pg_num+=1
    else:
        break

print("VN list acquired. Retrieving tags from every VN.")

for vn in vn_list:
    url='https://vndb.org/{}'.format(vn)
    r=requests.get(url)
    data=r.text
    soup=BeautifulSoup(data, 'html5lib')
    tag_list=[]
    for tags in soup.find_all('a'):
        if tags.get('href')[:2]=='/g':
            tag_list+=[tags.get_text()]
    for x in tag_list[1:]:
        if tag_dict.get(x)==None:
            tag_dict[x]=1
        else:
            tag_dict[x]+=1
    

# for x in tag_dict.keys():
#     y=re.search("[lL]oli",x)
#     if y!=None:
#         print(x,tag_dict[x])

tag_table=[[tag_dict[x],x] for x in tag_dict.keys()]
tag_table.sort(reverse=True)

with open('your_tags.csv', 'w', newline='') as csvfile:
    w=csv.writer(csvfile)
    for x in tag_table:
        w.writerow([x[1],x[0]])

print("Done! Your csv file should be present.")





    
    



