import csv
import pandas as pd
from jobspy import scrape_jobs

# Define your search terms and other parameters
search_terms = [
    "Software engineer",
    "cybersecurity analyst",
    "Python developer",
    "Java developer",
    "Django developer",
    "DevOps engineer"
]

location = "Nairobi"
results_wanted = 30
hours_old = 24

all_jobs = []

# Loop through each search term and scrape jobs
for search_term in search_terms:
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
    )

    # Add a column to identify the search term
    jobs['search_term'] = search_term

    # Append the jobs to the all_jobs list
    all_jobs.append(jobs)

# Concatenate all the dataframes into one
all_jobs_df = pd.concat(all_jobs, ignore_index=True)

# Save to CSV
all_jobs_df.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

print(f"Found {len(all_jobs_df)} jobs")
print(all_jobs_df.head())
