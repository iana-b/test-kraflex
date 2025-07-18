import os
import requests
import time
from db import create_table, insert_participant
from dotenv import load_dotenv
from html import unescape

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "apikey": API_KEY
}


def get_page_data(page):
    """
    Sends a GET request to the event API for a specific page.
    Returns JSON data with exhibitors.
    """
    url = "https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search"
    params = {
        "language": "de-DE",
        "q": "",
        "orderBy": "name",
        "pageNumber": page,
        "pageSize": 30,
        "orSearchFallback": "false",
        "showJumpLabels": "true",
        "findEventVariable": "EUROBIKE"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка на странице {page}: {e}")
    return None


def get_exhibitors_info():
    """
    Loads exhibitors data from all API pages.
    Returns a list of dictionaries with company details.
    """
    exhibitors = []
    data = get_page_data(1)
    if data is None:
        return exhibitors
    exhibitors.extend(parse_hits(data))

    # Calculate the total number of pages based on metaData
    total = data["result"]["metaData"]["hitsTotal"]
    per_page = data["result"]["metaData"]["hitsPerPage"]
    pages = (total // per_page) + (1 if total % per_page else 0)

    for page in range(2, pages + 1):
        time.sleep(0.5)
        data = get_page_data(page)
        if data is None:
            continue
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


create_table()
participants = get_exhibitors_info()
for p in participants:
    insert_participant(p)

print(f"Total participants added to the database: {len(participants)}")
