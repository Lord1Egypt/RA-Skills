#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SleepWindDownCoach, handle


def test_bedtime_detection():
    coach = SleepWindDownCoach('I want to be asleep by 10:30 pm, but I usually answer work email until 11:15 pm.')
    assert coach.desired_bedtime == '10:30 pm'
    assert coach.ladder_minutes == 60


def test_screen_boundary_mentions_work_email():
    coach = SleepWindDownCoach('I keep checking work email late at night before bed.')
    assert 'work email' in coach.environment['screens'].lower()


def test_output_sections():
    output = handle('Build me a wind-down plan because I scroll until midnight and feel wired.')
    assert output.startswith('# Wind-Down Plan')
    assert '## Ramp-Down Timeline' in output
    assert '## Environment Checklist' in output
    assert '## Morning Feedback' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
