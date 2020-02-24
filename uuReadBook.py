import requests
from bs4 import BeautifulSoup
import urllib.request
import random
import time
import fileinput
import csv
from opencc import OpenCC
cc = OpenCC('s2t')
listOfBook=[]
with open('books.csv', newline='') as csvfile:
     book = csv.reader(csvfile)
     for row in book:
         listOfBook=listOfBook+row
headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
           "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]

bookNum=0
url='https://sj.uukanshu.com/book.aspx?id='
urlHead=url[0:24]
while bookNum<len(listOfBook):
	url='https://sj.uukanshu.com/book.aspx?id='+listOfBook[bookNum]
	bookNum+=1
	user_agent = random.choice(headerlist)
	headers = {'User-Agent': user_agent}
	#index
	html=requests.get(url,headers=headers)
	html.encoding = 'utf-8'
	index=BeautifulSoup(html.text, 'lxml')
	indexURL=index.find(id="chapterList").find_all('a')
	bookName=cc.convert(index.find('h1',class_="bookname").text)
	print('Now proccessing:'+bookName)
	print('this is book number '+str(bookNum))
	if index.find(id="pages clear"):
		Page=index.find(id="pages clear").text
		numberOfindex=int(Page[-4])
	else:
		numberOfindex=1

	
	chapterURL=[]
	chapterNAME=[]
	for chapter in indexURL:
		chapterURL.append(chapter.get('href'))
		chapterNAME.append(chapter.text)
		
	if numberOfindex>1:
		page=2
		while page<=numberOfindex:
			url=url+"&page="+str(page)
			html=requests.get(url,headers=headers)
			html.encoding = 'utf-8'
			index=BeautifulSoup(html.text, 'lxml')
			indexURL=index.find(id="chapterList").find_all('a')	
			for chapter in indexURL:
				chapterURL.append(chapter.get('href'))
				chapterNAME.append(chapter.text)
			page+=1

	'''
	print(urlHead)
	print(chapterURL)
	print('length:'+str(len(chapterURL)))
	print(chapterNAME)
	print('length:'+str(len(chapterNAME)))
	'''
	HTTPsession = requests.Session()
	countor=0
	checkFlap=True
	#while checkFlap:
	C= open(bookName+".txt","w+",encoding="utf-8")
	while countor<len(chapterURL):
	#while countor<10:
		url=urlHead+chapterURL[countor]
		title=chapterNAME[countor]
		print('Now proccessing:'+bookName)
		print('this is book number '+str(bookNum))
		print('working on '+str(countor)+'/'+str(len(chapterURL)))
		countor+=1
		user_agent = random.choice(headerlist)
		headers = {'User-Agent': user_agent}
		html=HTTPsession.get(url,headers=headers)
		html.encoding = 'utf-8'

		att=BeautifulSoup(html.text, 'lxml')
		nextpagehtml=att.find(id="read_next")
		checkFlap=isinstance(nextpagehtml, str)
		#if checkFlap :	
		#nextpage=nextpagehtml.get('href')
		if att.find(id="bookContent") :C.write(title+att.find(id="bookContent").text)	
		#time.sleep(0.5)
		

	C.close() 
	C= open(bookName+".txt","r",encoding="utf-8")
	filedata = C.read()
	C.close() 
	filedata = filedata.replace("Ｕ","u")
	filedata = filedata.replace("U","u")
	filedata = filedata.replace("ｗ","w")
	filedata = filedata.replace("ｕ","u")
	filedata = filedata.replace("ｋ","k")
	filedata = filedata.replace("ａ","a")
	filedata = filedata.replace("ｎ","n")
	filedata = filedata.replace("ｓ","s")
	filedata = filedata.replace("ｈ","h")
	filedata = filedata.replace("ｃ","c")
	filedata = filedata.replace("ｏ","o")
	filedata = filedata.replace("ｍ","m")
	filedata = filedata.replace("．",".")
	filedata = filedata.replace("uu看书www.uukanshu.com"," ")
	filedata = filedata.replace("uu看书 www.uukanshu.com"," ")
	filedata = filedata.replace("uu看書www.uukanshu.com"," ")
	filedata = filedata.replace("uu看書 www.uukanshu.com"," ")
	filedata = filedata.replace("章节缺失、错误举报"," ")
	print("S2Ting")
	filedata=cc.convert(filedata)
	C= open(bookName+".txt","w",encoding="utf-8")
	C.write(filedata)
	C.close()
