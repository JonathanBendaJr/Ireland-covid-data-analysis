# Please Note that this file is schedule to run daily as task on python anywhere.


import requests, os
from bs4 import BeautifulSoup

URL = "https://opendatageohive.hub.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"


def get_daily_data():
    
    filename= "covid_data.csv"
    
    if os.path.exists(filename):
        os.remove(filename)
        
        page = requests.get(URL)        
        with open("COVID-19_HPSC_Detailed_Statistics_Profile.csv", "wb") as f:
            f.write(page.content)
        
        os.rename("COVID-19_HPSC_Detailed_Statistics_Profile.csv", filename)
        
    else:
        page = requests.get(URL)
        with open("COVID-19_HPSC_Detailed_Statistics_Profile.csv", "wb") as f:
            f.write(page.content)
            
        os.rename("COVID-19_HPSC_Detailed_Statistics_Profile.csv", filename)
        
    
    return page