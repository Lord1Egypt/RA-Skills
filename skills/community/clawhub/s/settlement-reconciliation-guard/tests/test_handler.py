#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SettlementReconciliationGuard, handle


def _skill_description() -> str:
    text = Path(__file__).resolve().parents[1].joinpath('SKILL.md').read_text(encoding='utf-8')
    frontmatter = text.split('---', 2)[1]
    for line in frontmatter.splitlines():
        if line.strip().startswith('description:'):
            return line.split(':', 1)[1].strip().strip("\"'")
    raise AssertionError('description not found in SKILL.md')


def test_review_mode_detection_month_end():
    guard = SettlementReconciliationGuard('Need month-end close support for payout and refund timing review.')
    assert guard.review_mode == 'Month-end close support'
    assert 'Refund timing mismatch' in guard.discrepancies


def test_discrepancy_detection_missing_payout_and_fee():
    guard = SettlementReconciliationGuard('Investigate missing payout, fee mismatch, and unreconciled batch differences.')
    assert guard.review_mode == 'Discrepancy investigation'
    assert 'Missing payout or delayed remittance' in guard.discrepancies
    assert 'Fee mismatch' in guard.discrepancies


def test_channel_and_evidence_detection():
    guard = SettlementReconciliationGuard('Compare Amazon payout report with bank statement and fee schedule before posting to the ERP general ledger.')
    assert 'Marketplace settlement' in guard.channels
    assert 'Bank payout / remittance' in guard.channels
    assert 'ERP / finance ledger' in guard.channels
    assert 'Payout report' in guard.evidence
    assert 'Bank statement' in guard.evidence
    assert 'Fee schedule' in guard.evidence


def test_render_contains_sections_and_skill_description():
    output = handle('Create a weekly exception sweep for refund, reserve, and fee variance issues.')
    assert output.startswith('# Settlement Reconciliation Guard')
    assert f'**Skill description:** {_skill_description()}' in output
    assert '## Matching Logic Table' in output
    assert '## Discrepancy Queue' in output
    assert '## Close Controls' in output


def test_dict_input_supported():
    output = handle({
        'review_mode': 'daily settlement check',
        'channels': ['marketplace', 'bank'],
        'evidence': ['payout report', 'bank statement', 'refund log'],
        'issue': 'chargeback reserve leakage',
    })
    assert '# Settlement Reconciliation Guard' in output
    assert 'Daily payout check' in output
    assert 'Chargeback or reserve leakage' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
