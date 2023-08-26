import os
import sys
import requests as req
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored

os.system('color')


def banner(total):
	print(r'''


  ___     __                                 __           
 / _ \___/ /__ ___ __  ___ ___ ___ _________/ /  ___ ___
/ // / _  / _ `/ // / (_-</ -_) _ `/ __/ __/ _ \/ -_) __/
\___/\_,_/\_,_/\_, (_)___/\__/\_,_/_/  \__/_//_/\__/_/  
              /___/                                          
                        0day.searcher
    [ Github  ] https://github.com/validverify/0day.searcher
    [ Version ] Version 1.0  @  validverify
    [ Date  ] ''' + str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + '''
    [ DB records ] 0day.today -> ''' + str(total) + '''
	''')


def get_page(query, filter_=False):
	ses = req.Session()
	ses.post("https://0day.today/", data={"agree": "Yes%2C+I+agree"})

	if not filter_:
		return ses.get(f"https://0day.today/search?search_request={query}").text
	else:
		return ses.get(f"https://0day.today/search?search_request={query}&search_type=1&category=-1&platform=-1&price_from=0&price_to=10000&author_login=&cve={filter_[0]}").text


def get_risk_color(item):
	if item == "CRITICAL":
		return "\033[41m \033[30m" + item
	if item == "HIGHT":
		return "\033[101m \033[30m" + item
	if item == "MEDIUM":
		return "\033[43m \033[30m" + item
	if item == "LOW":
		return "\033[42m \033[30m" + item
	if item == "UNDEFINED":
		return "\033[100m \033[30m" + item

def get_verify_color(status):
	if status == "OK":
		return "\033[32m" + status + "\033[0m"
	else:
		return "\033[31m" + status + "\033[0m"


def get_data(el):
	date = el[0].find("a").text
	name = el[1].find("a").text
	link = el[1].find("a")['href']

	platform = el[2].find("a")
	if platform == None:
		platform = "UNDEFINED"
	else:
		platform = platform.text

	risk_lvl = int(el[4].find("img")['src'][-5])
	if risk_lvl == 4:
		risk = "CRITICAL"
	if risk_lvl == 3:
		risk = "HIGHT"
	if risk_lvl == 2:
		risk = "MEDIUM"
	if risk_lvl == 1:
		risk = "LOW"
	if risk_lvl == 0:
		risk = "UNDEFINED"

	download = el[6].find("a")['href']
	CVE = el[7].find("div", attrs = {'class': 'TipText'}).text.replace(' ', '').replace('\t', '').replace('\n', '')

	verify_img = el[8].find("img")['src'][-6]
	if verify_img == 'c':
		verify = "OK"
	else:
		verify = "NO"

	author = el[10].find("a").text

	return [date, name, link, platform, risk, download, CVE, verify, author]


def print_info(list_, paint=False, to_file=False):
	print("[INFO] Structure : date name link platform risk download INFO: CVE verify author\n")
	res = []

	for i in list_:
		el = i.find_all("div", attrs = {'class': 'td'})
		res.append(get_data(el))

	if not to_file:
		for i in res:
			if not paint:
				print(f"\033[10m{i[0]}\033[0m \033[4m{i[1]} {i[2]}\033[46m\033[30m {i[3].upper()} \033[0m" + 
					get_risk_color(i[4])
					+ f" \033[0m\033[7m DOWNLOAD: {i[5]} \033[0mINFO: {i[6]} \033[0m" +
					get_verify_color(i[7])
					+ f" \033[93m{i[8]}\033[0m")
			else:
				print(f"{i[0]}\033[0m \033[4m{i[1]}\033[0m {i[2]} {i[3].upper()} {i[4]} DOWNLOAD: {i[5]} INFO: {i[6]} {i[7]} {i[8]}")
	else:
		to_file.write("Results by 0day.searcher from 0day.today website\nDate: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n\n")
		for i in res:
			to_file.write(f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]} {i[8]}\n")


def print_help():
	print('''
SMALL HELPY

Command structure: python 0day-searcher.py -flag1 -flag2=SOMETHING YOUR QUERY

Commands:

-h - Show help message and exit.
-c - Print results WITHOUT colors.
-CVE=CVE-Year-Number - Filter with CVE.
-O=FILE_NAME.extension - Write all output to file.
		''')



try:
	query = ""
	filt = []
	C = False
	F = False

	for i in range(len(sys.argv)):
		if i == 0:
			continue

		if sys.argv[i] == "-h":
			print_help()
			exit()
			continue
		elif sys.argv[i] == "-c":
			C = True
			continue
		elif sys.argv[i][0:3] == "-O=":
			F = open(str(sys.argv[i][3:len(sys.argv[i])]), 'w', encoding='utf-8')
			continue
		elif sys.argv[i][0:5] == "-CVE=":
			filt = [sys.argv[i][5:len(sys.argv[i])]]
			continue
		elif (sys.argv[i][0] == "-" and (sys.argv[i][1:len(sys.argv[i])] not in ['c', 'CVE', 'h', 'O'])):
			print("[ERROR] NO_SUCH_FLAG! Reason: Check this one -> " + str(sys.argv[i]) + " Fix: Check helpy below.")
			print_help()
			exit()
			continue

		if i == (len(sys.argv)-1):
			query = query + sys.argv[i]
		else:
			query = query + sys.argv[i] + " "
except IndexError:
	print("[ERROR] NO_ARGUMENTS! Fix: Enter command like this -> python 0day-searcher.py -flag1 -flag2=SOMETHING YOUR QUERY")
	exit()

print("[INFO](0day.today) Creating session and making request...")
soup = BeautifulSoup(get_page(query, filt), "html.parser")
banner(soup.find("div", attrs = {'class': 'menu'}).find("span", attrs = {'class': 'RedText'}).text)
print("[INFO](0day.today) Searching...")
list_ = soup.find_all("div", attrs = {'class': 'ExploitTableContent'})
if len(list_) == 0:
	print(f"\n[INFO](0day.today) Data with query \"{query}\" not found!")
	exit()
print_info(list_, C, F)