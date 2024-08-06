import pandas as pd

from jobsearch import scrape_jobs


def test_all():
    result = scrape_jobs(
        site_name=[
            "linkedin",

        ],
        search_term="engineer",
        results_wanted=5,
    )

    assert (
        isinstance(result, pd.DataFrame) and len(result) == 15
    ), "Result should be a non-empty DataFrame"
