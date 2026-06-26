#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ReturnReasonMiner, handle


def test_review_mode_detection_launch():
    miner = ReturnReasonMiner('We need launch issue triage for our new skincare product because returns are rising.')
    assert miner.review_mode == 'Launch Issue Triage'


def test_product_context_and_reason_detection_apparel_fit():
    miner = ReturnReasonMiner('Apparel returns mention size too small and fit mismatch across several variants.')
    assert miner.product_context == 'Apparel'
    assert 'Size or fit mismatch' in miner.reason_clusters


def test_reason_detection_damage_and_wrong_item():
    miner = ReturnReasonMiner('Customers report damaged packages and wrong items from the warehouse.')
    assert 'Shipping damage' in miner.reason_clusters
    assert 'Wrong item or fulfillment error' in miner.reason_clusters


def test_render_contains_sections():
    output = handle('Create a weekly return review for electronics returns and refund notes.')
    assert output.startswith('# Return Reason Mining Brief')
    assert '## Reason Taxonomy' in output
    assert '## Fix Priorities' in output
    assert '## Cross-Functional Action Plan' in output


def test_dict_input_supported():
    output = handle({
        'product_context': 'beauty',
        'review_mode': 'weekly return review',
        'reasons': ['damaged', 'not as described'],
        'signals': ['review', 'packaging'],
    })
    assert '# Return Reason Mining Brief' in output
    assert 'Beauty / Personal Care' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
