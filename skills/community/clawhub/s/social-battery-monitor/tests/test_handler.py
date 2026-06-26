#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_drained_input_flags_low_battery():
    output = handle('I am drained and I still have a networking event tonight')
    assert '# Social Battery Plan' in output
    assert '- Current level: Low' in output or '- Current level: Depleted' in output


def test_dict_input_renders_events():
    output = handle({
        'current_level': 'Moderate',
        'events': ['Family gathering', 'Friend catch-up']
    })
    assert 'Family gathering' in output
    assert 'Friend catch-up' in output


def test_output_contains_exit_line_and_recharge_menu():
    output = handle('Too many meetings and a birthday party this week')
    assert '- Exit line:' in output
    assert '## Recharge Menu' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
