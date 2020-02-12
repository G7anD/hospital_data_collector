import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


url = "https://www.yellowpages.uz/rubrika/bolnicy-i-kliniki/tashkent?pagenumber=1&pagesize=100"

def process(text):
	os.system('cls' if os.name == 'nt' else 'clear')
	if text == "loading":
		process(".")
		process("..")
		process("...")
	else:
		print(text)

process("Getting html page from url...")

data = requests.get(url)

bhtml = BeautifulSoup(data.content, 'html.parser')
objects = bhtml.find_all(class_='organizationBlock')

data_lists = []
counter = True
process("Starting filtering html objects")
for subItem in objects:
	sub_list = []

	for p in subItem.find_all(class_="greyText"):
		if counter:
		# is phone number
			for text in p.find_all("p", class_="text16 lh23"):
				sub_list.append([number.text for number in text.find_all("a") if number.text!=None])
			counter = False

		elif counter==False:
			p_ = p.find_all("p")
			name = p_[1].text
			a_list = [k.find("a") for k in p_[2].find_all("span")]
			address = [text.text for text in a_list if text!=None]	
			capt = lambda capt: [cap.capitalize() for cap in capt]
			sub_list.append([" ".join(capt(name.split(": ")[1].split())), " ".join(capt(address))])
			counter = True
		process("loading")

	else:
		data_lists.append(sub_list)
		process("loading")


process("Filtering has been comlated!")
process("Starting sorting")
data = []
for k in data_lists:
	data.append([k[-1][0], k[-1][1], k[0][0]])
	process("loading")


process("Exporting to csv...")
# df = pd.DataFrame(data=data, columns=["Name", "Address", "Phone number"], index=range(len(data_lists)))
# df.to_csv("hospital_database.csv")

process("Data collecting and saving has been complated!")