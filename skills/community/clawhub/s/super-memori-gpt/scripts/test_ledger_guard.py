#!/usr/bin/env python3
"""Deterministic synthetic regression cases; no external actions or credentials."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from ledger_guard import validate


def ledger():
    return {
        'schema_version': 2, 'project_id': 'synthetic-alpha', 'objective': 'Check revised drawing',
        'updated_at': '2026-09-26T10:00:00+00:00', 'status': 'active',
        'work_state': {'next_action': 'Inspect terminal mapping in revision B'},
        'constraints': [{'id': 'C1', 'text': 'Preserve exact terminal labels', 'status': 'active', 'source_ref': 'synthetic/user/1'}],
        'artifacts': [{'id': 'A1', 'name': 'drawing', 'version_or_fingerprint': 'B', 'state': 'verified', 'verification_scope': 'terminal mapping', 'source_ref': 'synthetic/drawing/B'}],
        'checks': [{'id': 'T1', 'status': 'passed', 'applicability': 'current', 'scope': 'terminal mapping', 'evidence_ref': 'synthetic/test/1', 'targets': [{'id': 'A1', 'version': 'B'}]}],
        'decisions': [], 'memories': [], 'relations': [],
    }


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.data = ledger()

    def bad(self, fragment):
        result = validate(self.data)
        self.assertFalse(result['ok'])
        self.assertTrue(any(fragment in e['message'] for e in result['errors']), result)

    def test_valid_current_checkpoint(self):
        self.assertTrue(validate(self.data)['ok'])

    def test_duplicate_id(self):
        self.data['decisions'] = [copy.deepcopy(self.data['constraints'][0])]
        self.bad('duplicate')

    def test_foreign_project(self):
        self.data['constraints'][0]['project_id'] = 'synthetic-beta'
        self.bad('different project')

    def test_missing_source(self):
        self.data['constraints'][0].pop('source_ref')
        self.bad('source/evidence')

    def test_proposal_is_not_fact(self):
        self.data['decisions'] = [{'id': 'D1', 'text': 'Maybe use option 2', 'status': 'proposed'}]
        self.assertTrue(validate(self.data)['ok'])

    def test_wrong_revision(self):
        self.data['checks'][0]['targets'][0]['version'] = 'A'
        self.bad('another artifact version')

    def test_history_is_preserved(self):
        self.data['checks'][0]['targets'][0]['version'] = 'A'
        self.data['checks'][0]['applicability'] = 'historical'
        self.data['artifacts'][0]['state'] = 'needs_recheck'
        self.assertTrue(validate(self.data)['ok'])

    def test_history_does_not_verify_current(self):
        self.data['checks'][0]['applicability'] = 'historical'
        self.bad('current passing check')

    def test_scope_mismatch(self):
        self.data['checks'][0]['scope'] = 'file readability only'
        self.bad('stated scope')

    def test_missing_check(self):
        self.data['checks'] = []
        self.bad('current passing check')

    def test_unresolved_link(self):
        self.data['relations'] = [{'from': 'C1', 'type': 'depends_on', 'to': 'unknown'}]
        self.bad('unresolved relation')

    def test_supersession_marking(self):
        self.data['decisions'] = [{'id': 'D2', 'status': 'active', 'text': 'Use C', 'source_ref': 'synthetic/user/2'}]
        self.data['relations'] = [{'from': 'D2', 'type': 'supersedes', 'to': 'C1'}]
        self.bad('marked superseded')

    def test_transitive_dependency(self):
        self.data['memories'] = [
            {'id': 'M1', 'status': 'active', 'source_ref': 'synthetic/1', 'depends_on': [{'id': 'A1', 'version': 'A'}]},
            {'id': 'M2', 'status': 'active', 'source_ref': 'synthetic/2', 'depends_on': [{'id': 'M1'}]},
        ]
        result = validate(self.data)
        paths = {e['path'] for e in result['errors'] if 'stale dependency' in e['message']}
        self.assertEqual(paths, {'memories[0]', 'memories[1]'})

    def test_recheck_resolves_structural_conflict(self):
        self.data['memories'] = [{'id': 'M1', 'status': 'needs_recheck', 'source_ref': 'synthetic/1', 'depends_on': [{'id': 'A1', 'version': 'A'}]}]
        self.assertTrue(validate(self.data)['ok'])

    def test_dependency_version_required(self):
        self.data['constraints'][0]['depends_on'] = [{'id': 'A1'}]
        self.bad('exact version')

    def test_cycle_terminates(self):
        self.data['constraints'][0]['depends_on'] = [{'id': 'C1'}]
        self.assertTrue(validate(self.data)['ok'])

    def test_reversed_interval(self):
        self.data['constraints'][0].update(valid_from='2026-09-26T00:00:00+09:00', valid_to='2026-09-25T00:00:00+09:00')
        self.bad('interval is reversed')

    def test_unknown_time_allowed(self):
        self.data['constraints'][0]['valid_from'] = None
        self.assertTrue(validate(self.data)['ok'])

    def test_timezone_required(self):
        self.data['constraints'][0]['valid_from'] = '2026-09-26T00:00:00'
        self.bad('timezone')

    def test_incomplete_project_needs_next_action(self):
        self.data['work_state']['next_action'] = None
        self.bad('unfinished project')

    def test_completed_project_may_have_no_next_action(self):
        self.data['status'] = 'completed'
        self.data['work_state']['next_action'] = None
        self.assertTrue(validate(self.data)['ok'])

    def test_secret_value_not_echoed(self):
        fake = 'sk-' + 'synthetic0' * 4
        self.data['constraints'][0]['text'] = fake
        result = validate(self.data)
        self.assertFalse(result['ok'])
        self.assertNotIn(fake, json.dumps(result))

    def test_signed_url_rejected(self):
        self.data['constraints'][0]['source_ref'] = 'https://example.invalid/source?sig=synthetic-value'
        self.bad('credential')

    def test_legacy_needs_explicit_migration(self):
        self.data['schema_version'] = 1
        self.bad('migrate old ledgers')

    def test_malformed_fields_report_without_crash(self):
        self.data['status'] = []
        self.data['constraints'][0]['status'] = {}
        self.data['relations'] = [{'type': []}]
        self.data['checks'][0]['applicability'] = {}
        self.assertFalse(validate(self.data)['ok'])

    def test_cli_stdin_and_exit_status(self):
        cli = str(Path(__file__).with_name('ledger_guard.py'))
        good = subprocess.run([sys.executable, cli, '-'], input=json.dumps(self.data), text=True, capture_output=True)
        self.assertEqual(good.returncode, 0)
        self.assertTrue(json.loads(good.stdout)['ok'])
        bad = subprocess.run([sys.executable, cli, '-'], input='{broken', text=True, capture_output=True)
        self.assertEqual(bad.returncode, 1)
        self.assertFalse(json.loads(bad.stdout)['ok'])
        self.assertEqual(bad.stderr, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
