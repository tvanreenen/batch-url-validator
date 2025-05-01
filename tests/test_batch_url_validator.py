import pandas as pd
import numpy as np
from src.batch_url_validator import check_url_status
import requests
from unittest.mock import patch

def test_check_success():
    with patch('requests.head') as mock_head, patch('requests.get') as mock_get:
        mock_head.return_value.status_code = 200
        assert check_url_status("http://example.com") == 200
        
        mock_head.return_value.status_code = 404
        assert check_url_status("http://example.com") == 404
        
        mock_head.return_value.status_code = 403
        mock_get.return_value.status_code = 200
        assert check_url_status("http://example.com") == 200

def test_check_errors():
    with patch('requests.head') as mock_head, patch('requests.get') as mock_get:
        mock_head.side_effect = requests.exceptions.Timeout()
        assert check_url_status("http://example.com") == 408
        
        mock_head.side_effect = requests.exceptions.RequestException()
        assert check_url_status("http://example.com") is None

def test_csv_processing(tmp_path):
    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({
        "url": ["http://example.com", "http://nonexistent.com"]
    })
    df.to_csv(csv_path, index=False)
    
    with patch('src.batch_url_validator.check_url_status') as mock_check:
        mock_check.side_effect = [200, pd.NA]
        
        # Import and run main here to avoid circular imports
        from src.batch_url_validator import main
        import sys
        sys.argv = ["batch_url_validator.py", str(csv_path)]
        main()
        
        # Verify results
        result_df = pd.read_csv(csv_path, dtype={'code': 'Int64'})
        assert result_df['code'].tolist() == [200, pd.NA]
        assert not result_df['datetime'].isna().any() 