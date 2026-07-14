"""
Sanity tests for Phase 1 components.

Verifies loading, profiling, and cleaning functionalities using safe encoding characters.
"""

import sys
import os
import pandas as pd
import numpy as np

# Ensure path is mapped correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics.data_loader import load_dataset
from analytics.cleaning import remove_duplicates, fill_missing, convert_datatypes
from analytics.profiling import dataset_summary, column_summary, statistics_report
from services.dataset_service import DatasetService


def test_analytics_profiling_and_cleaning():
    print("Running basic data pipeline validations...")

    # Create dummy dataset
    data = {
        "A": [1, 2, 2, np.nan, 5],
        "B": ["cat", "dog", "dog", "mouse", "cat"],
        "C": ["2026-01-01", "2026-01-02", "2026-01-02", "2026-01-04", "2026-01-05"],
    }
    df = pd.DataFrame(data)

    # Test summary profiling
    summary = dataset_summary(df)
    assert summary["rows"] == 5
    assert summary["columns"] == 3
    assert summary["duplicate_rows"] == 1
    assert summary["missing_cells"] == 1
    print("SUCCESS: Profiling dataset_summary validation passed.")

    # Test columns summary
    col_sum = column_summary(df)
    assert len(col_sum) == 3
    print("SUCCESS: Profiling column_summary validation passed.")

    # Test duplicates cleaning
    cleaned_dups = remove_duplicates(df)
    assert len(cleaned_dups) == 4
    print("SUCCESS: Cleaning remove_duplicates validation passed.")

    # Test missing value filling
    filled_df = fill_missing(df, "A", "constant", fill_value=10.0)
    assert filled_df["A"].isnull().sum() == 0
    assert filled_df["A"].iloc[3] == 10.0
    print("SUCCESS: Cleaning fill_missing validation passed.")

    # Test type conversion
    converted_df = convert_datatypes(df, "C", "datetime")
    assert pd.api.types.is_datetime64_any_dtype(converted_df["C"])
    print("SUCCESS: Cleaning convert_datatypes validation passed.")

    # Test service integration
    service_profile = DatasetService.get_profile(df)
    assert service_profile["summary"]["rows"] == 5
    print("SUCCESS: DatasetService.get_profile validation passed.")

    print("\nAll pipeline validations completed successfully!")


if __name__ == "__main__":
    test_analytics_profiling_and_cleaning()
