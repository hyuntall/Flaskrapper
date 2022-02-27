import csv

def save_to_file(jobs):
    file = open(f"{jobs}-jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for job in jobs:
        writer.writerow([job["title"], job["company"], job["url"]])
    return