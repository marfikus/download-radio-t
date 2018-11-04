# -*- coding: utf-8 -*-

import requests
import bs4
import wget
import os
import sys

def enter_number():
	while True:
		s = input("Enter the number or 'q' for quit: ")
		# s = s.strip()
		
		# if s == "":
			# continue
		
		if s == "q":
			quit()
			
		try:
			n = int(s)
			return n
		except ValueError:
			print("It is not a number!")


# path_to_file = os.getcwd()
# print(path_to_file)

file_with_number = "radio_t_number.txt"

if not os.path.exists(file_with_number):
	print("The file with number is not found!")
	number = enter_number()
	# print(number)
else:
	with open(file_with_number, "r", encoding="utf-8") as file:
		s = file.readline()
	try:
		number = int(s) + 1
		print("Number from file:	", number - 1)
	except ValueError:
		print("Uncorrect data from file!")		
		number = enter_number()

needed_name = "rt_podcast" + str(number)
print("Needed name:		", needed_name)

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
audio_arr = page.find_all("audio", limit=5)
# print(len(audio_arr))
# print(audio_arr)

del(page)
del(request)
del(requests)
del(bs4)

object_is_found = False

for audio in audio_arr:
	obj_link = audio["src"]
	
	if needed_name in obj_link:
		print("Object link:		", obj_link)
		object_is_found = True
		break

if not object_is_found:
	print("The object is not found!")
	quit()

file_name = wget.filename_from_url(obj_link)

dir_to_save = "/"
if sys.platform == "win32":
	dir_to_save = "D:\\Downloads\\"
elif sys.platform == "linux":
	dir_to_save = "/storage/sdcard0/Download/"
	
print("Directory to save:	", dir_to_save)

if not os.path.exists(dir_to_save):
	print("Directory to save not found!")
	quit()

if not os.path.exists(dir_to_save + file_name):
	wget.download(obj_link, dir_to_save + file_name)
	# print("download...")
	with open(file_with_number, "w", encoding="utf-8") as file:
		file.write(str(number))
else:
	print("This file already downloaded!")
	quit()
	
	