#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import TrendDemandForecaster, handle


def test_mode_detection_promo():
    forecaster = TrendDemandForecaster('Build a holiday promo demand forecast for our campaign launch and sale period.')
    assert forecaster.mode == 'Promo Lift Planning'


def test_signal_detection_inventory_and_conversion():
    forecaster = TrendDemandForecaster('Review conversion, checkout rate, stock coverage, and inbound risk for next month.')
    assert 'Conversion / Funnel' in forecaster.signals
    assert 'Inventory / Availability' in forecaster.signals


def test_dict_input_supported():
    output = handle({
        'objective': 'replenishment forecast',
        'horizon': 'next quarter',
        'signals': ['inventory', 'traffic'],
        'notes': 'Need a cautious base, upside, downside view before placing purchase orders.',
    })
    assert '# Trend Demand Forecast Brief' in output
    assert '## Scenario View' in output


def test_render_contains_sections():
    output = handle('Forecast whether demand is recovering or just normalizing after stockouts and markdowns.')
    assert output.startswith('# Trend Demand Forecast Brief')
    assert '## Leading Indicators' in output
    assert '## Assumptions and Limits' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
