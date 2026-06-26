#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ShippingCostOptimizer, handle


def test_primary_objective_detection_packaging():
    optimizer = ShippingCostOptimizer('Review our packaging waste, over-boxing, and carton sizes for ecommerce orders.')
    assert optimizer.primary_objective == 'Packaging rationalization'


def test_signal_detection_weight_and_region():
    optimizer = ShippingCostOptimizer('We need to analyze parcel weight, volumetric pricing, remote region surcharges, and carrier quotes.')
    assert 'Order weight / volume' in optimizer.signals
    assert 'Region mix / surcharge' in optimizer.signals
    assert 'Carrier pricing' in optimizer.signals


def test_render_contains_sections():
    output = handle('Should we raise the free-shipping threshold and review carrier routing?')
    assert output.startswith('# Shipping Cost Optimization Report')
    assert '## Optimization Opportunities' in output
    assert '## Pilot Recommendations' in output


def test_dict_input_supported():
    output = handle({
        'weights': '0.8kg average',
        'carrier': 'SF and YTO',
        'policy': 'free shipping above 59',
    })
    assert '# Shipping Cost Optimization Report' in output
    assert 'free shipping above 59' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
