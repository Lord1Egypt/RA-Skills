#!/usr/bin/env python3
"""Unit tests for doc_parser module."""
import json
from pathlib import Path
import sys
import pytest
import pandas as pd
sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from scripts.doc_parser import detect_and_load, load_csv, load_json, load_text, load_markdown, fallback_chain, with_retry

@pytest.fixture
def sample_csv(tmp_path):
    p = tmp_path / "test.csv"
    pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [90, 85]}).to_csv(p, index=False)
    return str(p)

@pytest.fixture
def sample_json(tmp_path):
    p = tmp_path / "test.json"
    p.write_text(json.dumps({"key": "value"}), encoding='utf-8')
    return str(p)

def test_load_csv(sample_csv):
    result = load_csv(sample_csv)
    assert result['type'] == 'spreadsheet'

def test_detect_and_load_csv(sample_csv):
    result = detect_and_load(sample_csv)
    assert result['_os'] in ('Windows', 'Darwin', 'Linux')

def test_fallback_chain():
    def ok(fp, **kw): return {'type': 'ok'}
    result = fallback_chain([('ok_strategy', ok)], 'dummy.txt')
    assert result['_strategy'] == 'ok_strategy'
