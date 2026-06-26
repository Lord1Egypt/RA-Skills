#!/usr/bin/env python3
"""Unit tests for viz_engine."""
from pathlib import Path
import sys
import pytest
sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from scripts.viz_engine import create_dashboard, create_network_graph, export_viz

@pytest.fixture
def sample_report():
    return {'distributions': {'revenue': {'mean': 100, 'median': 95, 'std': 20, 'min': 50, 'max': 200, 'q25': 80, 'q75': 120, 'skewness': 0.1, 'kurtosis': -0.2}}, 'anomalies': {}, 'correlations': {}, 'quality': {'missing_rate': {}, 'completeness': 0.95}}

def test_create_dashboard(sample_report):
    fig = create_dashboard(sample_report)
    assert fig is not None

def test_create_network():
    fig = create_network_graph([('A', 'B'), ('B', 'C')])
    assert fig is not None
