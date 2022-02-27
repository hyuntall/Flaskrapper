import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")


def write_company(company):
    file = open(f"jobs/{company['name']}.csv", mode="w", encoding="utf-8-sig")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for job in company["jobs"]:
      writer.writerow(list(job.values()))
    print(f"Completed....{company['name']}")


alba_url = "http://www.alba.co.kr"

alba_request = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_request.text, "html.parser")
main = alba_soup.find("div", {"id": "MainSuperBrand"})
brands = main.find_all("li", {"class": "impact"})
for brand in brands:
    link = brand.find("a", {"class": "goodsBox-info"})
    name = brand.find("span", {"class": "company"})
    if link and name:
        link = link["href"]
        name = name.text
        if "/" in name :
          name = name.replace("/"," ")
        company = {'name': name, 'jobs': []}
        jobs_request = requests.get(link)
        jobs_soup = BeautifulSoup(jobs_request.text, "html.parser")
        tbody = jobs_soup.find("div", {"id": "NormalInfo"}).find("tbody")
        rows = tbody.find_all("tr", {"class": ""})
        for row in rows:
            local = row.find("td", {"class": "local"})
            if local:
                local = local.text
            title = row.find("td", {"class": "title"})
            if title:
                title = title.find("a").find("span", {
                    "class": "company"
                }).text.strip()

            time = row.find("td", {"class": "data"})
            if time:
                time = time.text
            pay = row.find("td", {"class": "pay"})
            if pay:
                pay = pay.text
            date = row.find("td", {"class": "regDate"})
            if date:
                date = date.text
            job = {
                "place": local,
                "title": title,
                "time": time,
                "pay": pay,
                "date": date
            }
            company['jobs'].append(job)
        write_company(company)