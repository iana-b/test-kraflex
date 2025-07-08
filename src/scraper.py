import os
import requests
import time
from dotenv import load_dotenv
from html import unescape

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "apikey": API_KEY
}


def get_page_data(page):
    url = (f"https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/"
           f"search?language=de-DE&q=&orderBy=name&pageNumber={page}&pageSize=30"
           f"&orSearchFallback=false&showJumpLabels=true&findEventVariable=EUROBIKE")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data


def get_exhibitors_info():
    exhibitors = []
    data = get_page_data(1)
    exhibitors.extend(parse_hits(data))

    total = data["result"]["metaData"]["hitsTotal"]
    per_page = data["result"]["metaData"]["hitsPerPage"]
    pages = (total // per_page) + (1 if total % per_page else 0)

    for page in range(2, pages + 1):
        time.sleep(0.5)
        data = get_page_data(page)
        exhibitors.extend(parse_hits(data))

    return exhibitors


def parse_hits(data):
    exhibitors = []
    for hit in data["result"]["hits"]:
        exhibitor = hit["exhibitor"]
        company_name = exhibitor.get("name")
        if company_name:
            company_name = unescape(company_name)
        description = exhibitor.get("description", {}).get("text")
        country = exhibitor.get("address", {}).get("country", {}).get("label")
        website = exhibitor.get("homepage")
        email = exhibitor.get("address", {}).get("email")
        phone = exhibitor.get("address", {}).get("tel")

        exhibitors.append({
            "company_name": company_name,
            "description": description,
            "country": country,
            "website": website,
            "email": email,
            "phone": phone
        })
    return exhibitors


participants = get_exhibitors_info()
for p in participants:
    print(p)
