#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ServiceQaCoach, handle


def test_review_mode_detection_escalation():
    coach = ServiceQaCoach('Refund escalations are rising and we need an escalation reduction plan.')
    assert coach.review_mode == 'Escalation Reduction'


def test_channel_detection_chat_email():
    coach = ServiceQaCoach('Audit our live chat and email service quality this month.')
    assert 'Live chat' in coach.channels
    assert 'Email support' in coach.channels


def test_focus_and_issue_detection():
    coach = ServiceQaCoach('Agents sound robotic, responses are slow, and notes are incomplete.')
    assert 'Empathy and tone' in coach.focus_areas
    assert 'Response speed' in coach.focus_areas
    assert 'Weak case notes' in coach.issue_flags


def test_render_contains_sections():
    output = handle('Build a QA scorecard and coaching plan for our support team.')
    assert output.startswith('# Service QA Coaching Brief')
    assert '## Scorecard Rubric' in output
    assert '## Coaching Plan' in output
    assert '## Calibration and Sampling Plan' in output


def test_dict_input_supported():
    output = handle({
        'channel': ['chat', 'marketplace'],
        'goal': 'csat recovery',
        'issues': ['slow response', 'wrong policy'],
        'team_context': 'new hire queue',
    })
    assert '# Service QA Coaching Brief' in output
    assert 'CSAT Recovery' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
