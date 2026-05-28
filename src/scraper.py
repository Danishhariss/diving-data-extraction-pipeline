import re
import time
from pathlib import Path

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from config import (
    URL,
    HEADLESS,
    WAIT_TIME,
    TARGET_ATHLETES,
    DEBUG_HTML
)


def initialize_driver():
    """
    Initialize Selenium Chrome driver
    """

    chrome_options = Options()

    if HEADLESS:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--start-maximized")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )


def open_results_page(driver):
    """
    Open World Aquatics results page
    """

    print("Opening webpage...")

    driver.get(URL)

    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(5)

    handle_cookie_popup(driver)

    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.results-table__table--dv--format")
        )
    )

    print("Webpage loaded successfully.")


def handle_cookie_popup(driver):
    """
    Handle cookie popup if present
    """

    try:

        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Accept All') or contains(., 'Deny')]"
                )
            )
        )

        button.click()

        print("Cookie popup handled.")

        time.sleep(2)

    except Exception:

        print("No cookie popup found.")


def click_target_expand_buttons(driver):
    """
    Click '+' expandable button for target athletes
    """

    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "tr.results-table__row")
        )
    )

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "tr.results-table__row"
    )

    print(f"Found {len(rows)} result rows")

    for row in rows:

        row_text = row.text.upper()

        for athlete in TARGET_ATHLETES:

            if athlete.upper() in row_text:

                try:

                    expand_button = row.find_element(
                        By.CSS_SELECTOR,
                        "button.js-results-row-expand"
                    )

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});",
                        expand_button
                    )

                    time.sleep(1)

                    driver.execute_script(
                        "arguments[0].click();",
                        expand_button
                    )

                    print(f"Clicked '+' button for {athlete}")

                    time.sleep(2)

                except Exception as error:

                    print(
                        f"Failed to click '+' button for {athlete}: {error}"
                    )


def save_debug_html(driver):
    """
    Save rendered HTML for debugging
    """

    Path("outputs").mkdir(exist_ok=True)

    with open(DEBUG_HTML, "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    print(f"Debug HTML saved to: {DEBUG_HTML}")


def clean_text(element):
    """
    Clean HTML text
    """

    if element is None:
        return None

    return " ".join(
        element.get_text(" ", strip=True).split()
    )


def parse_results_from_html(html):
    """
    Parse structured dive results from HTML
    """

    soup = BeautifulSoup(html, "html.parser")

    records = []

    main_table = soup.select_one(
        "table.results-table__table--dv--format"
    )

    if main_table is None:
        raise ValueError("Main results table not found.")

    tbody = main_table.select_one(
        "tbody.results-table--Finals"
    )

    if tbody is None:
        raise ValueError("Finals table body not found.")

    rows = tbody.find_all("tr", recursive=False)

    for index in range(0, len(rows), 2):

        athlete_row = rows[index]

        if index + 1 >= len(rows):
            continue

        expandable_row = rows[index + 1]

        cells = athlete_row.find_all(
            "td",
            recursive=False
        )

        if len(cells) < 6:
            continue

        rank = clean_text(cells[0])

        country = clean_text(cells[1])

        athlete = clean_text(cells[2])

        age = clean_text(cells[3])

        final_points = clean_text(cells[4])

        points_behind = clean_text(cells[5])

        # Dynamically remove ranking number
        athlete = re.sub(
            r"\(\d+\)",
            "",
            athlete
        ).strip()

        if athlete not in TARGET_ATHLETES:
            continue

        sub_rows = expandable_row.select(
            "tr.results-table__sub-row"
        )

        for sub_row in sub_rows:

            sub_cells = sub_row.find_all("td")

            if len(sub_cells) < 12:
                continue

            records.append({

                "athlete": athlete,

                "country": country,

                "rank": rank,

                "age": age,

                "final_points": final_points,

                "points_behind": (
                    0
                    if points_behind == "-"
                    else points_behind
                ),

                "dive_round": clean_text(sub_cells[0]),

                "dive_code": clean_text(sub_cells[1]),

                "difficulty": clean_text(sub_cells[2]),

                "judge_1": clean_text(sub_cells[3]),

                "judge_2": clean_text(sub_cells[4]),

                "judge_3": clean_text(sub_cells[5]),

                "judge_4": clean_text(sub_cells[6]),

                "judge_5": clean_text(sub_cells[7]),

                "judge_6": clean_text(sub_cells[8]),

                "judge_7": clean_text(sub_cells[9]),

                "dive_score": clean_text(sub_cells[10]),

                "cumulative_score": clean_text(sub_cells[11]),
            })

    return records


def run_scraper():
    """
    Execute full scraping pipeline
    """

    driver = initialize_driver()

    try:

        open_results_page(driver)

        click_target_expand_buttons(driver)

        save_debug_html(driver)

        records = parse_results_from_html(
            driver.page_source
        )

        print(
            f"Structured records extracted: {len(records)}"
        )

        return records

    finally:

        time.sleep(3)

        driver.quit()
