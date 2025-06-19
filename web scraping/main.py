import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
from collections import Counter

# Base URL with pagination
base_url = "https://www.motravay.mu/jobs?page={}"

# to count job listings per company and per date
company_job_count = Counter()
date_job_count = Counter()

# Open a CSV file for writing
with open("Job_listings2.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Title", "Company", "Date Posted"])
    for page_number in range(1, 7):  # to scrape the pages
        URL = base_url.format(page_number)
        page = requests.get(URL)
        if page.status_code != 200:
            print(f"Failed to retrieve page {page_number}")
            continue

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="job-listings")
        if not results:
            print(f"No job listings found on page {page_number}")
            continue

        job_elements = results.find_all("div", class_="row")
        for job_element in job_elements:
            title_element = job_element.find("a", class_="job-details-link")
            company_element = job_element.find("a", class_="job-info-link-item")
            date_element = job_element.find("div", class_="job-posted-date")

            # Handle cases where elements might be missing
            title = title_element.text.strip() if title_element else "No Title"
            company = company_element.text.strip() if company_element else "No Company"
            date = date_element.text.strip() if date_element else "No Date"

            # Write a row of data
            writer.writerow([title, company, date])

            # Count job listings per company and per date
            if company != "No Company":
                company_job_count[company] += 1
            if date != "No Date":
                date_job_count[date] += 1

        print(f"Page {page_number} scraped successfully.")

# Generate the bar chart for job listings per company
if company_job_count:
    companies = list(company_job_count.keys())
    job_counts = list(company_job_count.values())

    plt.figure(figsize=(10, 6))
    plt.bar(companies, job_counts, color='hotpink')
    plt.xlabel('Company')
    plt.ylabel('Number of Job Listings')
    plt.title('Number of Job Listings per Company')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout to make room for rotated x-axis labels
    plt.savefig("Job_listings_per_company.png")
    plt.show()

    # Generate the pie chart for job listings per company
    custom_colors = ['red', 'coral', 'orange', 'gold', 'yellow', 'greenyellow', 'lime',
                     'aquamarine', 'turquoise', 'cyan', 'deepskyblue', 'royalblue', 'blue', 'navy',
                     'blueviolet', 'violet', 'fuchsia', 'deeppink', 'pink']
    plt.figure(figsize=(14, 14))
    plt.pie(job_counts, labels=companies, autopct='%1.1f%%', startangle=180, colors=custom_colors)
    plt.title('Distribution of Job Listings per Company')
    plt.tight_layout()  # Adjust layout for the pie chart
    plt.savefig("Job_listings_pie_chart.png")
    plt.show()

# Generate the bar chart for job listings per day
if date_job_count:
    dates = list(date_job_count.keys())
    job_counts_by_date = list(date_job_count.values())

    plt.figure(figsize=(10, 6))
    plt.bar(dates, job_counts_by_date, color='skyblue')
    plt.xlabel('Date Posted')
    plt.ylabel('Number of Job Listings')
    plt.title('Number of Job Listings per Day')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout to make room for rotated x-axis labels
    plt.savefig("Job_listings_per_day.png")
    plt.show()

    # Generate the pie chart for job listings per day
    plt.figure(figsize=(14, 14))
    plt.pie(job_counts_by_date, labels=dates, autopct='%1.1f%%', startangle=160, colors=custom_colors)
    plt.title('Distribution of Job Listings per Day')
    plt.tight_layout()  # Adjust layout for the pie chart
    plt.savefig("Job_listings_pie_chart_by_day.png")
    plt.show()
else:
    print("No job listings were found to plot.")
