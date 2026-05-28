````markdown
# Diving Data Extraction Pipeline

## Project Overview

This project was developed to automate the extraction of diving competition results from the World Aquatics website.

The extraction pipeline focuses on:

- Men's 10m Platform
- Final Round
- Selected athletes:
  - Yuming BAI
  - Randal WILLARS VALDEZ

The extracted data is transformed into a structured analytical dataset and exported into CSV and Excel formats.

---

# Objectives

The main objectives of this project are:

- Automate dynamic web data extraction
- Handle expandable result sections using Selenium
- Parse structured dive information from rendered HTML
- Transform extracted data into analysis-ready format
- Export clean datasets for downstream analytics

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Selenium | Browser automation and dynamic interaction |
| BeautifulSoup | HTML parsing |
| Pandas | Data transformation and export |
| WebDriver Manager | Automatic ChromeDriver management |

---

# Project Structure

```text
diving_data_scraping/
│
├── outputs/
│   ├── diving_scores.csv
│   ├── diving_scores.xlsx
│   └── debug_page.html
│
├── src/
│   ├── config.py
│   ├── scraper.py
│   ├── transform.py
│   └── main.py
│
├── requirements.txt
└── README.md
````

---

# Extraction Workflow

## 1. Browser Automation

Selenium is used to:

* Open the World Aquatics results webpage
* Wait for dynamic content to load
* Automatically click the expandable "+" button for target athletes

---

## 2. HTML Capture

After expansion:

* The fully rendered HTML DOM is captured
* HTML is saved for debugging and validation purposes

---

## 3. HTML Parsing

BeautifulSoup is used to:

* Traverse athlete result rows
* Locate expandable dive result sections
* Extract:

  * Athlete information
  * Dive code
  * Degree of difficulty
  * Judge scores
  * Dive score
  * Cumulative score

---

## 4. Data Transformation

The extracted records are transformed into a structured Pandas DataFrame.

Each row represents:

```text
One athlete dive attempt
```

This structure enables future analysis such as:

* Performance consistency analysis
* Difficulty comparison
* Judge scoring analysis
* Competition trend analysis

---

## 5. Export

Final outputs are exported into:

* CSV format
* Excel format

---

# Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

# Execution

Run the pipeline using:

```bash
python src/main.py
```

---

# Output

Generated outputs:

| File               | Description                 |
| ------------------ | --------------------------- |
| diving_scores.csv  | Structured diving dataset   |
| diving_scores.xlsx | Excel version of dataset    |
| debug_page.html    | Rendered HTML for debugging |

---

# Scalability

The scraper was designed modularly.

Future extensions may include:

* Additional athletes
* Different competition categories
* Multiple event extraction
* Automated scheduling
* Dashboard integration

Configuration is controlled through:

```python
URL
TARGET_ATHLETES
```

allowing the extraction logic to remain reusable across events.

---

# Notes

This project demonstrates:

* Dynamic web scraping
* Browser automation
* DOM parsing
* Structured data engineering workflow
* Analytical dataset preparation

```
```
