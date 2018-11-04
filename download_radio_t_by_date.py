# -*- coding: utf-8 -*-

import requests
import bs4
import datetime
import wget
import os
import sys

current_date = datetime.date.today()
timedelta = datetime.timedelta(days=1)
needed_date = str(current_date - timedelta)
print("Needed date for search:	", needed_date)

link_for_request = "https://radio-t.com"
print("Request to:		", link_for_request)
request = requests.get(link_for_request)
print("Request status code:	", request.status_code)
# print(request.encoding)

if request.status_code != 200:
	quit()

request.encoding = "utf-8"	# !for correct work with Russian text
page = bs4.BeautifulSoup(request.text, "html.parser")
# page = bs4.BeautifulSoup(request.text, "lxml")
articles = page.find_all("article", limit=3)
# print(len(articles))

del(page)
del(request)
del(requests)
del(bs4)
del(datetime)

object_is_found = False

for article in articles:
	# date_of_publication = article.header.find("time")["datetime"]
	date_of_publication = article.select("header time")[0]["datetime"]
	# if date_of_publication == "2018-06-16T18:31:16Z":
	if needed_date in date_of_publication:
		# print("ok")
		audio = article.select(".entry-content audio")
		if len(audio) > 0:
			# print(len(audio))
			obj_link = audio[0]["src"]
			print("Object link:		", obj_link)
			object_is_found = True
			break
			
if not object_is_found:
	print("The object is not found!")
	quit()
	
#====================================
# first variant for download file:

# split_link = link.split("/") # !!!
# file_name = split_link[-1]
# print(file_name)
# audio_request = requests.get(obj_link)
# with open("D:\\Downloads\\" + file_name, "wb") as file:
	# file.write(audio_request.content)
	
# print(audio_request.status_code)
# print(audio_request.headers["content-type"])
# print(audio_request.encoding)
#====================================

dir_to_save = "/"
if sys.platform == "win32":
	dir_to_save = "D:\\Downloads\\"
elif sys.platform == "linux":
	dir_to_save = "/storage/sdcard0/Download/"
	
print("Directory to save:	", dir_to_save)

if not os.path.exists(dir_to_save):
	print("Directory to save not found!")
	quit()

file_name = wget.filename_from_url(obj_link)

if not os.path.exists(dir_to_save + file_name):
	wget.download(obj_link, dir_to_save + file_name)
else:
	print("This file already downloaded!")
	quit()

