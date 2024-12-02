# README for FRED Data Processing Scripts

## Overview
This repository contains three Python scripts designed to interact with the FRED (Federal Reserve Economic Data) API to collect, process, and store economic data. The scripts retrieve top-level economic data categories, download specific data series, and organize the data into structured formats.

---

## 1. `categories.py`
**Purpose:**  
Fetches and stores top-level and sub-level category information from the FRED API.

**Key Features:**
- Connects to the FRED API using an API key.
- Retrieves all top-level categories and their subcategories recursively.
- Stores the collected data in `fred_categories.json`.

**Execution:**
```bash
python categories.py
```
**Output:**
 `fred_categories.json` — Contains the entire category hierarchy from FRED.

## 2. known_IDs.py
**Purpose:**  
Downloads time-series data for pre-defined economic indicators (e.g., GDP, CPI) using their known FRED series IDs.

**Key Features:**
- Maps series IDs to descriptions and data frequencies via the data_codes dictionary.
- Organizes the data by year and saves it in CSV format.
- Handles daily, monthly, and annual data granularity.

**Execution:**
```bash
python known_IDs.py
```
**Output:**
 Data files organized by indicator and year within the economic_data/ directory.

## 3. series.py
**Purpose:**
Fetches series data for all categories recursively from the FRED API and stores them in structured directories.

**Key Features:**
- Recursively navigates through FRED categories to download all associated series.
- Cleans up filenames to ensure compatibility across operating systems.
- Stores data for each category in series_data.json files within dynamically created directories.

**Execution:**
```bash
python series.py
```
**Output:**
 Structured directories named by category ID and name.
 Data files organized by indicator and year within the categories/ directory.

## Prerequisites
Python Libraries: Install the required libraries:
```bash
pip install requests pandas
```
API Key: Replace the placeholder api_key in each script with a valid FRED API key.

## Notes
- Ensure you have adequate permissions to write files to the working directory.
- Respect the FRED API's rate limits to avoid blocking requests.
- Modify the scripts as needed to add new indicators or handle additional data.

## License
This project is open-source and available under the MIT License.