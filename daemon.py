import requests
import time
import json
import sqlite3


def get_post_data(url, data={}, headers={}):
	r = requests.post(url, data=data, headers=headers)
	if str(r.status_code) == "200":
		return r.text
	else:
		print(r.status_code, r.reason)
		return "Error"

def get_get_data(url, data={}, headers={}):
	r = requests.get(url, data=data, headers=headers)
	if str(r.status_code) == "200":
		return r.text
	else:
		print(r.status, r.reason)
		return "Error"

def write_to_db(data):
	db = sqlite3.connect("./database.db")

	cursor = db.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,date TEXT,sensor1 INTEGER,sensor2 INTEGER,sensor3 INTEGER,sensor4 INTEGER)")
	
	cursor.execute("INSERT INTO data(date, sensor1, sensor2, sensor3, sensor4) VALUES (?,?,?,?,?)", (data["date"], data["sensor1"], data["sensor2"], data["sensor3"], data["sensor4"]))
	db.commit()

	db.close()		

def create_json():
	result = [[],[],[],[],[]]

	db = sqlite3.connect("./database.db")

	cursor = db.cursor()
	cursor.execute("SELECT * FROM data")

	for row in cursor:
		result[0].append(row[1])
		result[1].append(row[2])
		result[2].append(row[3])
		result[3].append(row[4])
		result[4].append(row[5])

	result_json = {
		"date": result[0],
		"sensor1": result[1],
		"sensor2": result[2],
		"sensor3": result[3],
		"sensor4": result[4]
	}

	with open("log_file.json", "w") as archive:
		json.dump(result_json, archive)

def main():

	password = input("Password: ")

	data = {
		"email": "valtteri.arhola@gmail.com",
		"password": password
	}

	headers = {
		"Content-type": "application/json"
	}
	url = "https://opendata.hopefully.works/api/"
	#login
	end = "login"
	path = url + end
	r = get_post_data(path, data)
	if r != "Error":
		print("Logged in successfully")

		jsonObj = json.loads(r)
		accessToken = jsonObj["accessToken"]

		headers["Authorization"] = "Bearer " + accessToken

		end = "events"
		path = url + end

		#reading the data
		while True:
			r = get_get_data(path, {}, headers)
			if r != "Error":
				info = json.loads(r)
				print(info["date"])

				write_to_db(info)
				create_json()

				time.sleep(3600)
			else:
				print("Something went wrong")
				break


if __name__ == "__main__":
	main()
