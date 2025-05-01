import argparse
import concurrent.futures
from datetime import datetime
import pandas as pd
import requests

def check_url_status(url):
    timeout = 2  # Reasonable timeout for most healthy servers
    try:
        # Try HEAD first - faster than GET as it only fetches headers
        status_code = requests.head(url, timeout=timeout).status_code 
        # Some servers reject HEAD requests with 400/403, but might work with GET
        if status_code in [400, 403]:
            status_code = requests.get(url, timeout=timeout).status_code
    except requests.exceptions.Timeout:
        status_code = 408  # Standard HTTP timeout status code
    except requests.exceptions.RequestException as e:
        status_code = None  # Any other request error (DNS, connection refused, etc.)

    return status_code

def main():
    parser = argparse.ArgumentParser(
        description='Check URLs in a CSV file for their status codes. The CSV must contain a "url" column. Status codes and check times will be added/updated.'
    )
    parser.add_argument('input_file', help='Path to the input CSV file (must contain a "url" column)')
    parser.add_argument('--max-workers', type=int, default=10, help='Maximum number of concurrent requests (default: 10)')
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input_file)
        if 'url' not in df.columns:
            print("Error: Input file must contain a 'url' column.")
            return
        if 'code' not in df.columns:
            df['code'] = None
        if 'datetime' not in df.columns:
            df['datetime'] = None
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: Input file '{args.input_file}' is empty.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Get all unique URLs to check
    urls_to_check = df['url'].unique().tolist()
    total_urls = len(urls_to_check)
    
    if total_urls == 0:
        print("No URLs to check - the file is empty.")
        return

    print(f"Checking {total_urls} URLs with {args.max_workers} concurrent workers...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = []
        for url in urls_to_check:
            futures.append(executor.submit(check_url_status, url=url))
        
        for url, future in zip(urls_to_check, futures):
            status_code = future.result()
            df.loc[df['url'] == url, 'code'] = status_code
            df.loc[df['url'] == url, 'datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        df.to_csv(args.input_file, index=False)
    except Exception as e:
        print(f"Error saving file: {e}")
        return

    print("\nLink Check Summary:")
    print(f"Total links checked: {total_urls}")
    print("\nStatus Code Distribution:")
    print(df['code'].value_counts())

if __name__ == "__main__":
    main()