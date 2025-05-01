# Batch URL Validator

A simple utility script to validate multiple URLs in parallel. I created this when I needed to check the status of a large number of links from documentation.

## Features

- Validates URLs in parallel using an adjustable amount of workers
- Updates a CSV file with status codes and timestamps

## Usage

1. Prepare a CSV file with a `url` column containing the links to check
2. Run the script:
```bash
uv run src/batch_url_validator.py your_list_of_urls.csv
```

Optional arguments:
- `--max-workers`: Number of concurrent requests (default: 10)
```bash
uv run src/batch_url_validator.py your_list_of_urls.csv --max-workers 20
```

## Output

The script will:
1. Update the input CSV file with:
   - `code`: HTTP status code (or None if the request failed)
   - `datetime`: Timestamp of when the check was performed
2. Print a summary of the results including:
   - Total number of links checked
   - Distribution of status codes

## Example

Input: `your_list_of_urls.csv`
```csv
url
https://example.com
https://nonexistent.example
```

After running:
```csv
url,code,datetime
https://example.com,200,2024-03-21 14:30:45
https://nonexistent.example,None,2024-03-21 14:30:46
```

## Notes

- The script checks all unique URLs in the file each time it runs
- Supports both HEAD and GET requests (falls back to GET if HEAD fails)
- Timeout is set to 2 seconds per request
- If a URL appears multiple times in the CSV, it will only be checked once, but all instances will be updated with the same status code and timestamp
