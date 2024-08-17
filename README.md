# Professor Scraper

This repository contains code to scrape information about specified classes from SJSU's class schedules and print that data.

## Setup

To get started, install the necessary dependencies:

```sh
python3 -m pip install -r requirements.txt
playwright install chromium
```

## Usage

To scrape all professors for ENGR 10 in Fall 2024, run the below.

```sh
python3 ./scrape.py https://www.sjsu.edu/classes/schedules/fall-2024.php "ENGR 10"
```

You can also filter by instruction type. If you just wanted LAB professors, you could run

```sh
python3 ./scrape.py https://www.sjsu.edu/classes/schedules/fall-2024.php "ENGR 10" --types LAB
```

If you wanted SEM and LEC instead, you could run

```sh
python3 ./scrape.py https://www.sjsu.edu/classes/schedules/fall-2024.php "ENGR 10" --types SEM LEC
```

By default, SEM, LEC, and LAB are the accepted class types.
