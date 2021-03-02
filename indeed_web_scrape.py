import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    """Generate a url with a given job position and location"""
    template = "https://www.indeed.com/jobs?q={}&l={}"
    url = template.format(position, location)
    return url


def get_record(job_card):
    """Retrieve each job card and display the records of each"""
    atag = job_card.h2.a
    job_title = atag.get("title")
    job_url = "http://indeed.com" + atag.get("href")
    company = job_card.find("span", "company").text.strip()
    location = job_card.find("div", "recJobLoc").get("data-rc-loc")
    job_summary = job_card.find("div", "summary").text.strip().replace("\n", "")
    date_posted = job_card.find("span", "date").text
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        job_salary = job_card.find("span", "salaryText").text.strip()
    except:
        AttributeError
        job_salary = "DNE"

    record = (job_title, company, location, job_summary, date_posted, job_url, job_salary, today)
    return(record)


def main(position, location):
    """This is the programs main function to return the jobs data"""
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", "jobsearch-SerpJobCard")
        
        try:
            url = "https://www.indeed.com" + soup.find("a", {"aria-label": "Next"}).get("href")
        except AttributeError:
            break

        for job_card in job_cards:
            record = get_record(job_card)
            records.append(record)

    #Upload each job record to a csv file called job_postings.csv
    with open("job_postings.csv", 'w', newline= "", encoding= "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Job Summary", "Date Posted",
        "Job Url", "Job Salary", "Todays Date"])
        writer.writerows(records)

#TO RUN PROGRAM SIMPLY INSERT DESIRED JOB TITLE AND JOB LOCATION
main("software developer", "kansas city")

    


    