#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_goal_and_waiting_node_are_rendered():
    result = handle({
        'skill_name': 'quest-chain-decomposer',
        'input': {
            'goal': 'Submit the school volunteer application',
            'deadline': 'Friday',
            'success_definition': 'The application is submitted with all supporting documents.',
            'blockers': 'Waiting for teacher approval',
        },
    })['result']
    assert 'Submit the school volunteer application' in result
    assert 'Starter Trio' in result
    assert 'Waiting node' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'quest-chain-decomposer', 'mode': 'prompt'})['result']
    assert 'quest chain' in result.lower()
    assert 'Definition of Done' in result


def test_string_input_is_supported():
    result = handle({'skill_name': 'quest-chain-decomposer', 'input': 'Goal: finish my tax form\nDeadline: this weekend\nBlockers: missing receipt'})['result']
    assert '# Quest Chain Map' in result
    assert 'finish my tax form' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
