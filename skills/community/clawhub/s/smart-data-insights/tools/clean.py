#!/usr/bin/env python3
"""
Data cleaning utilities.
"""

import pandas as pd
import numpy as np


def clean_data(df, remove_duplicates=True, handle_missing='auto', standardize=True):
    """
    Clean data with various strategies.
    
    Args:
        df: Input DataFrame
        remove_duplicates: Remove duplicate rows
        handle_missing: Strategy for missing values ('auto', 'drop', 'fill_mean', 'fill_median', 'fill_mode')
        standardize: Standardize column names and text data
    
    Returns:
        Cleaned DataFrame
    """
    df_cleaned = df.copy()
    
    # 1. Standardize column names
    if standardize:
        df_cleaned.columns = [
            col.strip().lower().replace(' ', '_').replace('-', '_')
            for col in df_cleaned.columns
        ]
    
    # 2. Remove duplicates
    if remove_duplicates:
        duplicates_before = df_cleaned.duplicated().sum()
        if duplicates_before > 0:
            df_cleaned = df_cleaned.drop_duplicates()
            print(f"Removed {duplicates_before} duplicate rows")
    
    # 3. Handle missing values
    if handle_missing == 'auto':
        for col in df_cleaned.columns:
            missing_pct = df_cleaned[col].isnull().sum() / len(df_cleaned)
            
            if missing_pct > 0.5:
                # Drop columns with >50% missing
                df_cleaned = df_cleaned.drop(columns=[col])
                print(f"Dropped column '{col}' ({missing_pct*100:.1f}% missing)")
            elif missing_pct > 0:
                # Fill based on data type
                if df_cleaned[col].dtype in ['int64', 'float64']:
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
                else:
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 'Unknown')
    
    elif handle_missing == 'drop':
        df_cleaned = df_cleaned.dropna()
    
    elif handle_missing == 'fill_mean':
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].mean())
    
    elif handle_missing == 'fill_median':
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())
    
    elif handle_missing == 'fill_mode':
        for col in df_cleaned.columns:
            if not df_cleaned[col].mode().empty:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    
    # 4. Standardize text data
    if standardize:
        text_cols = df_cleaned.select_dtypes(include=['object']).columns
        for col in text_cols:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
            df_cleaned[col] = df_cleaned[col].replace('nan', np.nan)
    
    # 5. Remove outliers (optional, conservative)
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df_cleaned[col].quantile(0.01)
        Q3 = df_cleaned[col].quantile(0.99)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        outliers = ((df_cleaned[col] < lower) | (df_cleaned[col] > upper)).sum()
        if outliers > 0 and outliers < len(df_cleaned) * 0.01:  # Only if <1% outliers
            df_cleaned[col] = df_cleaned[col].clip(lower, upper)
    
    return df_cleaned


def clean_column(series, strategy='auto'):
    """
    Clean a single column.
    
    Args:
        series: pandas Series
        strategy: 'auto', 'numeric', 'categorical', 'datetime'
    
    Returns:
        Cleaned Series
    """
    if strategy == 'auto':
        # Try to infer type
        try:
            return pd.to_numeric(series, errors='coerce')
        except:
            pass
        
        try:
            return pd.to_datetime(series, errors='coerce')
        except:
            pass
        
        return series
    
    elif strategy == 'numeric':
        return pd.to_numeric(series, errors='coerce')
    
    elif strategy == 'datetime':
        return pd.to_datetime(series, errors='coerce')
    
    return series
