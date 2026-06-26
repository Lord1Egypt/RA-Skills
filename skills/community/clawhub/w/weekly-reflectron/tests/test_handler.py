#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import WeeklyReflector, handle


def test_sleep_pattern_detection():
    reflector = WeeklyReflector('Poor sleep made work harder, but I still finished a draft and went for two walks.')
    assert reflector.pattern.startswith('Sleep and recovery')


def test_dimension_coverage():
    reflector = WeeklyReflector('Great client progress. Family dinner felt connected. Read two chapters of a book.')
    assert set(reflector.dimensions.keys()) == {'Work', 'Health', 'Relationships', 'Growth'}


def test_output_sections():
    output = handle('Finished a client draft, slept poorly, and had a good talk with my partner.')
    assert output.startswith('# Weekly Reflection')
    assert '### Work' in output
    assert '### Health' in output
    assert '### Relationships' in output
    assert '### Growth' in output
    assert '- One experiment:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
