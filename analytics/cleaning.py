"""
Data cleaning module.

Provides pure functions for cleaning Pandas DataFrames (removing duplicates,
handling missing values, converting datatypes, and renaming columns).
"""

from typing import Union, Dict, Any, List, Optional
import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    return df.drop_duplicates().reset_index(drop=True)


def fill_missing(
    df: pd.DataFrame,
    column: str,
    strategy: str,
    fill_value: Optional[Any] = None,
) -> pd.DataFrame:
    """
    Fill missing values in a specific column of a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to fill missing values in.
        strategy (str): Strategy to use ('mean', 'median', 'mode', 'constant', 'drop').
        fill_value (Optional[Any]): Constant value to fill if strategy is 'constant'.

    Returns:
        pd.DataFrame: DataFrame with missing values filled or dropped.
    """
    new_df = df.copy()

    if strategy == "mean":
        mean_val = new_df[column].mean()
        new_df[column] = new_df[column].fillna(mean_val)
    elif strategy == "median":
        median_val = new_df[column].median()
        new_df[column] = new_df[column].fillna(median_val)
    elif strategy == "mode":
        if not new_df[column].mode().empty:
            mode_val = new_df[column].mode()[0]
            new_df[column] = new_df[column].fillna(mode_val)
    elif strategy == "constant":
        if fill_value is not None:
            new_df[column] = new_df[column].fillna(fill_value)
    elif strategy == "drop":
        new_df = new_df.dropna(subset=[column]).reset_index(drop=True)

    return new_df


def convert_datatypes(
    df: pd.DataFrame, column: str, datatype: str
) -> pd.DataFrame:
    """
    Convert a specific column's data type.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        datatype (str): Target datatype ('int64', 'float64', 'str', 'datetime', 'category').

    Returns:
        pd.DataFrame: DataFrame with modified column datatype.
    """
    new_df = df.copy()

    if datatype == "datetime":
        new_df[column] = pd.to_datetime(new_df[column], errors="coerce")
    elif datatype in {"int64", "float64"}:
        new_df[column] = pd.to_numeric(new_df[column], errors="coerce")
        new_df[column] = new_df[column].astype(datatype)
    else:
        new_df[column] = new_df[column].astype(datatype)

    return new_df


def rename_columns(df: pd.DataFrame, columns_dict: Dict[str, str]) -> pd.DataFrame:
    """
    Rename columns based on a dictionary mapping old names to new names.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns_dict (Dict[str, str]): Dict mapping {"old_col_name": "new_col_name"}.

    Returns:
        pd.DataFrame: DataFrame with columns renamed.
    """
    return df.rename(columns=columns_dict)


def remove_empty_rows(
    df: pd.DataFrame, threshold: float = 0.5
) -> pd.DataFrame:
    """
    Remove rows where the percentage of missing values exceeds a threshold.

    Args:
        df (pd.DataFrame): Input DataFrame.
        threshold (float): Percentage threshold of missing data (0.0 to 1.0) to drop a row.
                           Default is 0.5 (drop row if 50% or more fields are null).

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    new_df = df.copy()
    limit = int((1 - threshold) * len(new_df.columns))
    return new_df.dropna(thresh=limit).reset_index(drop=True)
