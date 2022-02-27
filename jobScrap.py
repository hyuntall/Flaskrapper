from bs4 import BeautifulSoup as bs
import requests

def stackOverFlow(result, word):
    response = requests.get(f"https://stackoverflow.com/jobs?r=true&q={word}")
    soup = bs(response.text, "html.parser")
    jobList = soup.find("div", {"class": "listResults"})
    jobs = jobList.find_all("div", {"class": "flex--item fl1"})
    for job in jobs:
        h2 = job.find("h2")
        jobsName = h2.text.strip()
        company = job.find("h3").find("span").text.strip()
        link = h2.find("a")['href']
        applyLink = f"https://stackoverflow.com{link}"
        job = {
            "title": jobsName,
            "company": company,
            "url": applyLink
        }
        result.append(job)

def getJobsWWR(result, link):
    response = requests.get(link)
    soup = bs(response.text, "html.parser")
    jobs = soup.select(".jobs > article > ul > li")
    for i in range(1, len(jobs)-1):
        jobsName = jobs[i].find("span", {"class": "title"}).text.strip()
        company = jobs[i].find("span", {"class": "company"}).text.strip()
        link = jobs[i].find("a")["href"]
        applyLink = f"https://weworkremotely.com{link}"
        job = {
            "title": jobsName,
            "company": company,
            "url": applyLink
        }
        result.append(job)

def weWorkRemotely(result, word):
    response = requests.get(f"https://weworkremotely.com/remote-jobs/search?term={word}")
    soup = bs(response.text, "html.parser")
    section = soup.find_all("section", {"class": "jobs"})
    links = []
    for sect in section:
        viewAll = sect.find("li", {"class": "view-all"})
        link = f"https://weworkremotely.com{viewAll.find('a')['href']}"
        links.append(link)
        getJobsWWR(result, link)



def remoteOk():
    #remoteOk website not working... (503 error)
    while 1:
        response = requests.get("https://remoteok.com/remote-python-jobs")
        print("요청중")
        if response.status_code != 503:
            break
    soup = bs(response.text, "html.parser")
    page = soup.select("#page")
    jobs = soup.select("#jobsboard")
    print(response.status_code)

def getJobs(word):
    result = []
    stackOverFlow(result, word)
    weWorkRemotely(result, word)
    return result

if __name__ == '__main__':
    result = []
    #stackOverFlow()
    #weWorkRemotely()
    #remoteOk()
