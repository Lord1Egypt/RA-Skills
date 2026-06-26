#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SupportFlowBuilder, handle


def test_scenario_detection_delivery_delay():
    builder = SupportFlowBuilder('Create an email and chat flow for delivery delay tickets')
    assert builder.scenario == 'Delivery Delay'


def test_channel_detection_email_and_chat():
    builder = SupportFlowBuilder('Need email and live chat macros for a refund workflow')
    assert 'Email' in builder.channels
    assert 'Live Chat' in builder.channels


def test_scenario_detection_payment_failure():
    builder = SupportFlowBuilder('Design a bot handoff for payment failed support cases')
    assert builder.scenario in ('Payment Failure', 'Bot Handoff')


def test_render_contains_key_sections():
    output = handle('Build a return and exchange support flow with macros and governance notes')
    assert output.startswith('# Support Flow Design Pack')
    assert '## Support Flow Map' in output
    assert '## Macros / Canned Responses' in output
    assert '## Governance and QA' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
