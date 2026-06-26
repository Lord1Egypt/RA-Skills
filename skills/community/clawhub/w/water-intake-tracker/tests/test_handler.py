#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_hot_and_active_context_gets_higher_range():
    output = handle('I keep forgetting to drink water when it is hot and I work out most afternoons')
    assert '# Hydration Plan' in output
    assert '- Suggested range: 2.4 to 3.2 L' in output


def test_dict_input_preserves_pattern_and_tracking_method():
    output = handle({
        'current_pattern': 'Two cups in the morning and then I forget until dinner',
        'tracking_method': 'Cup count',
        'weather': 'Hot'
    })
    assert 'Two cups in the morning and then I forget until dinner' in output
    assert '- Cup, bottle, or tally system: Cup count' in output


def test_output_includes_catch_up_rule_and_watchouts():
    output = handle('Need a simple hydration routine with a bottle refill method')
    assert '- Catch-up rule:' in output
    assert '## Watch-outs' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
