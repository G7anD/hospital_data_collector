import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np

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

for k in data_lists:
	# if 
	print(address_list[0][0] in k[-1][1], k[-1][1])
	for region in address_list:
		if region[0] in k[-1][1]:
			data.append([k[-1][0], k[-1][1], k[0][0], region[1]])
	process("loading")


process("Exporting to csv...")
df = pd.DataFrame(data=data, columns=["Name", "Address", "Phone number"], index=range(len(data_lists)))
df.to_csv("hospital_database.csv")

process("Data collecting and saving has been complated!")

print(*data)

data = []
address_list = [["Алмазарский район", "41.3633985,69.2193817,15"],
				["Бектемирский район", "41.2351317,69.3325734,15"],
				["Мирабадский район", "41.2752288,69.285661,15"],
				["Мирзо-Улугбекский район", "41.3316969,69.3423533,15"],
				["Сергелийский район", "41.2112991,69.2244916,15"],
				["Учтепинский район", "41.2976196,69.1569859,15"],
				["Чиланзарский район", "41.2806198,69.1963778,15"],
				["Шайхантахурский район", "41.327136,69.1991659,15"],
				["Юнусабадский район", "41.3565092,69.2860369,15"],
				["Яккасарайский район", "41.278851,69.2399592,15"],
				["Яшнабадский район", "41.2836335,69.3052342,15"]]

df = pd.read_csv("Hospital data collector/hospital_database.csv")

data_lists = df.values.tolist()
for k in data_lists:
	for region in address_list:
		if region[0] in k[2]:
			data.append([k[1], k[2], k[3], region[1]])




header = {
	"Authorization": None
}

for d in data:
	data = {
			"name_uz": d[0],
			"name_en": d[0],
			"name_ru": d[0],
			"address_uz": d[1],
			"address_ru": d[1],
			"address_en": d[1],
			"place_point": d[3],
			"transports": " - ",
			"phone_number": d[2],
			"working_time": "09:00 - 19:00",
			"author": 1
		}
	res = requests.post("https://feeso.ru/api/hosp/add/", headers = header, data=data)
	print(res, res.text)


dff = pd.DataFrame(data=data, columns=["Nomi", "Manzili", "Kontakt nomeri", "Geo nuqtasi"], index=range(len(data)))
dff.to_csv("Tashkent_hospitals_list.csv")