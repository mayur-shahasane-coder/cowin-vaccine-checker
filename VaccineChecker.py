import requests
import datetime
from fake_useragent import UserAgent
from plyer.utils import platform
from plyer import notification
import time

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

pincodes = ["410206", "410207","410209"]
age = 18
num_of_days = 5

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(num_of_days)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

while True:
    for pincode in pincodes:
        for cr_date in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, cr_date)
            response = requests.get(URL, headers=browser_header)
            if response.ok:
                resp_json = response.json()
                if resp_json["centers"]:
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= age:
                                if session["available_capacity_dose1"] > 0 and center["fee_type"] == 'Free':
                                    notification.notify(
                                        title='Vaccine Available',
                                        message=f'''\nDate: {cr_date} \nCenter: {center["name"]} \nDose 1 Available: {session["available_capacity_dose1"]}''',
                                        app_name='Vaccine Checker'
                                        )
    time.sleep(300)
