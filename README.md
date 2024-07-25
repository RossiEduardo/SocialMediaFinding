# Artist Social Media Scraper

This project retrieves social media URLs (Instagram, Facebook, Twitter) for a list of artists using the Google Serper API and OpenAI's GPT models.

## Setup

    Replace "YOUR_API_KEY" with your Google Serper and OpenAI API keys in the code.

    Create a file named artists.txt in the same directory as the script. This file should contain a list of artist names, one per line.

## Requirements

To run this code, you need to install the Python libraries listed in the `requirements.txt` file. You can do this using the command:

```
pip install -r requirements.txt
```

## Usage

Run the Python script. The script reads artist names from the artists.txt file, searches for social media URLs for each artist using the Google Serper API and OpenAI model, and writes the results to a CSV file named social_medias.csv
```
python3 google_scrap.py
```
