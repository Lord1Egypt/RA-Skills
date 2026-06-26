#!/usr/bin/env python3
"""Unit tests for deep_analyzer."""
from pathlib import Path
import sys
import pytest
import pandas as pd
import numpy as np
sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from scripts.deep_analyzer import DeepAnalyzer, analyze_time_series

@pytest.fixture
def basic_df():
    np.random.seed(42)
    return pd.DataFrame({'revenue': np.random.normal(1000, 200, 50), 'cost': np.random.normal(600, 100, 50)})

def test_run_full_analysis(basic_df):
    report = DeepAnalyzer(basic_df).run_full_analysis()
    assert 'overview' in report and 'quality' in report

def test_distributions(basic_df):
    report = DeepAnalyzer(basic_df).run_full_analysis()
    assert 'revenue' in report['distributions']
