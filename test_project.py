import pytest
from datetime import datetime
import pandas as pd
from project import CSV, confirm_entry, add_corrected_entry


@pytest.fixture
def sample_csv():
    """Fixture to set up and clean up the CSV file."""
    CSV.CSV_FILE = "test_trucking_data.csv"
    CSV.initialize_csv()
    yield
    # Cleanup after tests
    import os
    if os.path.exists(CSV.CSV_FILE):
        os.remove(CSV.CSV_FILE)


def test_initialize_csv(sample_csv):
    """Test that the CSV file is correctly initialized."""
    data = CSV.get_data()
    assert list(data.columns) == CSV.COLUMNS
    assert data.empty


def test_add_entry(sample_csv):
    """Test adding an entry to the CSV file."""
    date = "01-12-2024"
    mileage = 200
    load_type = "Refrigerated"
    delivery_details = "Delivery to Cold Storage"
    
    CSV.add_entry(date, mileage, load_type, delivery_details)
    data = CSV.get_data()
    
    assert len(data) == 1
    assert data.iloc[0]["date"] == date
    assert data.iloc[0]["mileage"] == mileage
    assert data.iloc[0]["load_type"] == load_type
    assert data.iloc[0]["delivery_details"] == delivery_details


def test_get_data(sample_csv):
    """Test retrieving data from the CSV file."""
    date = "01-12-2024"
    mileage = 200
    load_type = "Refrigerated"
    delivery_details = "Delivery to Cold Storage"
    
    CSV.add_entry(date, mileage, load_type, delivery_details)
    data = CSV.get_data()
    
    assert not data.empty
    assert data.iloc[0]["date"] == date


def test_confirm_entry():
    """Test confirming an entry."""
    # Simulate user input for 'y' (yes)
    from unittest.mock import patch
    with patch("builtins.input", side_effect=["y"]):
        assert confirm_entry("01-12-2024", 200, "Refrigerated", "Delivery to Cold Storage") is True

    # Simulate user input for 'n' (no)
    with patch("builtins.input", side_effect=["n"]):
        assert confirm_entry("01-12-2024", 200, "Refrigerated", "Delivery to Cold Storage") is False


def test_add_corrected_entry():
    """Test adding a corrected entry."""
    from unittest.mock import patch
    inputs = [
        "01-12-2024",  # Date
        "200",         # Mileage
        "1",           # Load Type (Refrigerated)
        "Delivery to Cold Storage",  # Delivery Details
        "y",           # Confirm
    ]
    with patch("builtins.input", side_effect=inputs):
        date, mileage, load_type, delivery_details = add_corrected_entry()
        assert date == "01-12-2024"
        assert mileage == 200
        assert load_type == "Refrigerated"
        assert delivery_details == "Delivery to Cold Storage"
