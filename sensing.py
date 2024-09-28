import csv
import requests
import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import xml.etree.ElementTree as ET
import time
import random

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def check_rss_link(row, session):
    category, title, url = row
    max_retries = 3
    delay = 1

    for attempt in range(max_retries):
        try:
            if 'rsshub.app' in url:
                # Special handling for rsshub.app
                response = session.get(url, headers=get_headers(), timeout=10, allow_redirects=True)
            else:
                response = session.get(url, timeout=10, allow_redirects=True)
            
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if 'xml' in content_type or 'rss' in content_type or 'feed' in content_type:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    return row, True, "Valid RSS feed (feedparser)"
                
                try:
                    root = ET.fromstring(response.content)
                    if root.find('.//item') is not None or root.find('.//entry') is not None:
                        return row, True, "Valid RSS/Atom feed (XML parsing)"
                except ET.ParseError:
                    pass
            
            if 'json' in content_type:
                json_data = response.json()
                if isinstance(json_data, dict) and ('items' in json_data or 'entries' in json_data):
                    return row, True, "Valid JSON feed"
            
            return row, False, "No valid feed format detected"
        
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return row, False, f"Request error after {max_retries} attempts: {str(e)}"
            time.sleep(delay * (2 ** attempt) + random.uniform(0, 1))
        
        except Exception as e:
            return row, False, f"Error parsing feed: {str(e)}"

def validate_rss_links(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header row
        rows = list(csv_reader)

    results = []
    with requests.Session() as session:
        session.headers.update(get_headers())
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(check_rss_link, row, session) for row in rows]
            for future in tqdm(as_completed(futures), total=len(rows), desc="Checking RSS links"):
                results.append(future.result())

    return results

def main(input_file, output_file):
    print(f"Validating RSS links from {input_file}...")
    results = validate_rss_links(input_file)

    valid_links = [row for row, is_valid, _ in results if is_valid]
    invalid_links = [(row, reason) for row, is_valid, reason in results if not is_valid]

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Status', 'Category', 'Title', 'URL', 'Reason'])
        
        for row in valid_links:
            writer.writerow(['Valid'] + list(row))
        
        for row, reason in invalid_links:
            writer.writerow(['Invalid'] + list(row) + [reason])

    print(f"\nValidation complete. Results saved to {output_file}")
    print(f"Valid links: {len(valid_links)}")
    print(f"Invalid links: {len(invalid_links)}")

if __name__ == "__main__":
    input_file = "rss_links.csv"
    output_file = "rss_validation_results.csv"
    main(input_file, output_file)