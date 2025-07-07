import requests
from bs4 import BeautifulSoup

# https://eurobike.com/frankfurt/en/exhibitor-search.detail.html/hb-hightech-gmbh.html
# https://eurobike.com/frankfurt/de/ausstellersuche.detail.html/hb-hightech-gmbh.html

BASE_URL = "https://eurobike.com/frankfurt/de/"
# EXHIBITOR_URL = "ausstellersuche.detail.html/hb-hightech-gmbh.html"
EXHIBITOR_URL = "ausstellersuche/ausstellersuche.detail.html/nordic-passion-oy.html"


def parse_exhibitor_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    company_name = soup.select_one("h1.ex-exhibitor-detail__title-headline")
    company_name = company_name.text.strip() if company_name else None

    description = soup.select_one(".ex-text-image__copy p")
    description = description.text.strip() if description else None

    country = soup.select_one(".ex-contact-box__address-field-full-address")
    if country:
        lines = country.get_text(separator="\n").split("\n")
        country = lines[-1].strip()
    else:
        country = None

    website_tag = soup.select_one("a.ex-contact-box__website-link")
    website = website_tag["href"].strip() if website_tag else None

    email_tag = soup.select_one("a.ex-contact-box__contact-btn")
    if email_tag:
        href = email_tag.get("href", "")
        if href.startswith("mailto:"):
            email = href.replace("mailto:", "").split("?")[0].strip()
        else:
            email = None
    else:
        email = None

    phone_tag = soup.select_one("a.a-link.ex-contact-box__address-field-tel-number")
    if phone_tag:
        href = phone_tag.get("href", "")
        if href.startswith("tel:"):
            phone = href.replace("tel:", "")
        else:
            phone = None
    else:
        phone = None

    return {"company_name": company_name, "description": description, "country": country, "website": website,
            "email": email, "phone": phone}


data = parse_exhibitor_page(BASE_URL + EXHIBITOR_URL)
print(data)
