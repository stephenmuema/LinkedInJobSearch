import sqlite3
import pandas as pd
from jobsearch import scrape_jobs

# Define your search terms and other parameters
search_terms = [
    "Software engineer",
    # "DevOps Engineer",
    # "Site Reliability Engineer",
    # "SRE",
    "Python",
    "Django"
    # "Cyber Security Engineer",
    # "Cyber Security Analyst",

]

location = "Kenya"
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
print(all_jobs_df)
# Define the SQLite database connection
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# Define the table schema
create_table_query = '''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    site TEXT,
    job_url TEXT,
    job_url_direct TEXT,
    title TEXT,
    company TEXT,
    location TEXT,
    job_type TEXT,
    date_posted TEXT,
    salary_source TEXT,
    interval TEXT,
    min_amount REAL,
    max_amount REAL,
    currency TEXT,
    is_remote TEXT,
    job_level TEXT,
    job_function TEXT,
    company_industry TEXT,
    listing_type TEXT,
    emails TEXT,
    description TEXT,
    company_url TEXT,
    company_url_direct TEXT,
    company_addresses TEXT,
    company_num_employees TEXT,
    company_revenue TEXT,
    company_description TEXT,
    logo_photo_url TEXT,
    banner_photo_url TEXT,
    ceo_name TEXT,
    ceo_photo_url TEXT,
    search_term TEXT
);
'''

# Create the table
cursor.execute(create_table_query)


# Function to insert a single job row with error handling
def insert_job(cursor, job_row):
    placeholders = ', '.join(['?'] * len(job_row))
    columns = ', '.join(job_row.keys())
    sql = f"INSERT INTO jobs ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(sql, tuple(job_row))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting row {job_row['id']}: {e}")


# Insert each job row into the database
for _, job_row in all_jobs_df.iterrows():
    insert_job(cursor, job_row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Found {len(all_jobs_df)} jobs")
print(all_jobs_df.head())
