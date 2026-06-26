#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import WarehouseFlowOptimizer, handle


def test_focus_detection_replenishment():
    optimizer = WarehouseFlowOptimizer('Our forward-pick stockouts and replenishment delays are slowing every shift.')
    assert optimizer.focus == 'Replenishment Control'


def test_signal_detection_labor_and_cutoff():
    optimizer = WarehouseFlowOptimizer('We have headcount imbalance, late carrier cutoff misses, and staging congestion.')
    assert 'Labor Imbalance' in optimizer.signals
    assert 'Cutoff / Service Risk' in optimizer.signals


def test_dict_input_supported():
    output = handle({
        'objective': 'reduce picking congestion',
        'zones': ['pick module', 'packing wall'],
        'signals': ['queue', 'travel time'],
        'notes': 'Need quick wins before peak season.',
    })
    assert '# Warehouse Flow Optimizer Brief' in output
    assert '## 30-Day Pilot Plan' in output


def test_render_contains_sections():
    output = handle('Help me improve slotting, walking distance, and queueing before next day SLA starts slipping.')
    assert output.startswith('# Warehouse Flow Optimizer Brief')
    assert '## Quick Wins' in output
    assert '## Assumptions and Limits' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
