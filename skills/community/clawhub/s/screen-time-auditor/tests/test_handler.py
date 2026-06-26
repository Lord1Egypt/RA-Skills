#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_late_night_phone_pattern_is_detected():
    output = handle('I keep doomscrolling on my phone late at night when I am tired')
    assert '# Screen Time Audit' in output
    assert 'Late night' in output


def test_dict_input_supports_manual_audit_fields():
    output = handle({
        'devices': ['Phone', 'Laptop'],
        'apps': ['Short video apps', 'Messaging and checking'],
        'time_bands': ['Work transitions']
    })
    assert 'Phone, Laptop' in output
    assert 'Short video apps' in output


def test_output_contains_friction_and_target():
    output = handle('Too much checking between meetings on Slack and social media')
    assert '- Friction to add:' in output
    assert '- Weekly target:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
