#!/usr/bin/env python3
"""Unit tests for security_utils."""
from pathlib import Path
import sys
import pytest
import pandas as pd
sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from scripts.security_utils import DataMasker, SecureCleanup, secure_context

def test_mask_phone():
    m = DataMasker()
    assert '138****5678' in m.mask_string("13812345678")

def test_mask_dataframe():
    df = pd.DataFrame({'phone': ['13812345678']})
    masked = DataMasker().mask_dataframe(df)
    assert '****' in masked['phone'].iloc[0]

def test_secure_cleanup():
    c = SecureCleanup()
    d = c.create_temp_dir()
    c.cleanup_all()
    assert not d.exists()
