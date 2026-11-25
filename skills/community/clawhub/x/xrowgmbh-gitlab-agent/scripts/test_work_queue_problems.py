"""JSON-only discovery and read-only, non-secret problem diagnosis (#209)."""
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

DIRECTORY = Path(__file__).resolve().parent


def load():
    spec = importlib.util.spec_from_file_location('problems', DIRECTORY / 'work-queue-problems.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProblemTests(unittest.TestCase):
    def setUp(self):
        self.module = load()
        self.active = self.module.active

    def test_missing_email_is_structured_deduplicated_and_never_printed(self):
        issue = {'iid': 7, 'project_id': 1, 'web_url': 'https://gitlab.example.test/team/app/-/work_items/7', 'author': {'id': 88, 'username': 'alice'}}
        out, err = io.StringIO(), io.StringIO()
        with patch.object(self.active, 'configured_accept_entries', return_value=['@example.test']), \
                patch.object(self.active, 'accepted_usernames', return_value=set()), \
                patch.object(self.active, 'assignment_candidates', return_value=[issue, issue]), \
                patch.object(self.active, 'api_json', return_value={'id': 88, 'public_email': '', 'token': 'private-secret'}), \
                patch.object(self.active, 'synchronize_forbidden') as labels, \
                patch.object(self.active.subprocess, 'run') as mutation, \
                redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(self.active.assign_unassigned_items(1, 'robot', 'owner', {}, dry_run=True), [])
        mutation.assert_not_called()
        labels.assert_not_called()
        self.assertEqual((out.getvalue(), err.getvalue()), ('', ''))
        self.assertEqual(len(self.active.PROBLEMS), 1)
        problem = self.active.PROBLEMS[0]
        self.assertEqual((problem['code'], problem['user_id']), ('author-email-unavailable', 88))
        self.assertIn('explicit username/group', problem['remedy'])
        self.assertNotIn('private-secret', json.dumps(problem))
        self.assertEqual(problem['user_username'], 'alice')
        self.assertEqual(problem['user_url'], 'https://gitlab.example.test/alice')
        self.assertEqual(problem['project_path'], 'team/app')
        self.assertEqual(problem['issue_url'], 'https://gitlab.example.test/team/app/-/issues/7')
        self.assertEqual(problem['issue_iid'], 7)

    def test_problem_context_rejects_private_and_unsafe_values(self):
        self.active.record_problem('author-email-unavailable', user_id=True,
            user_username='<img onerror=attack>', project_path='../bad',
            user_url='javascript:attack()', issue_url='https://token@gitlab.test/x',
            email='secret@example.test', token='private-token', raw='private-response')
        self.assertEqual(set(self.active.PROBLEMS[0]), {'code', 'severity', 'message', 'remedy'})

    def test_lookup_failure_retains_public_example_without_accepting_author(self):
        issue = {'iid': 7, 'project_id': 1, 'web_url': 'https://gitlab.example.test/team/app/-/issues/7',
                 'author': {'id': 88, 'username': 'alice'}}
        with patch.object(self.active, 'configured_accept_entries', return_value=['@example.test']), \
                patch.object(self.active, 'accepted_usernames', return_value=set()), \
                patch.object(self.active, 'assignment_candidates', return_value=[issue, issue]), \
                patch.object(self.active, 'api_json', side_effect=ValueError('private-token')), \
                patch.object(self.active.subprocess, 'run') as mutation:
            self.assertEqual(self.active.assign_unassigned_items(1, 'robot', 'owner', {}, dry_run=True), [])
        mutation.assert_not_called()
        self.assertEqual(len(self.active.PROBLEMS), 1)
        self.assertEqual(self.active.PROBLEMS[0]['user_username'], 'alice')
        self.assertEqual(self.active.PROBLEMS[0]['project_path'], 'team/app')
        self.assertNotIn('private-token', json.dumps(self.active.PROBLEMS))

    def test_accepted_candidate_is_diagnosed_without_mutating(self):
        issue = {'iid': 7, 'author': {'id': 88, 'username': 'alice'}}
        with patch.object(self.active, 'configured_accept_entries', return_value=['alice']), \
                patch.object(self.active, 'accepted_usernames', return_value={'alice'}), \
                patch.object(self.active, 'assignment_candidates', return_value=[issue]), \
                patch.object(self.active, 'synchronize_forbidden') as labels, \
                patch.object(self.active.subprocess, 'run') as mutation:
            self.active.assign_unassigned_items(1, 'robot', 'owner', {}, dry_run=True)
        mutation.assert_not_called()
        labels.assert_not_called()
        self.assertEqual(self.active.PROBLEMS, [])

    def test_report_uses_read_only_mode_and_clears_previous_problems(self):
        self.active.record_problem('author-email-unavailable', user_id=1)
        with patch.object(self.active, 'configured_owner', return_value='owner'), \
                patch.object(self.module.queue, 'read_api', return_value={'id': 9, 'username': 'robot'}), \
                patch.object(self.module.queue, 'report', return_value={}), \
                patch.object(self.active, 'assign_unassigned_items') as scan:
            result = self.module.report()
        scan.assert_called_once_with(9, 'robot', 'owner', {}, dry_run=True)
        self.assertEqual(result['problems'], [])
        self.assertIn('generated_at', result)

    def test_failed_assigned_scan_is_reported_without_hiding_collaborator_diagnostics(self):
        def scan(*_args, **kwargs):
            self.assertEqual(kwargs, {'dry_run': True})
            self.active.record_problem('author-email-unavailable', user_id=88)
        with patch.object(self.active, 'configured_owner', return_value='owner'), \
                patch.object(self.module.queue, 'read_api', return_value={'id': 9, 'username': 'robot'}), \
                patch.object(self.module.queue, 'report', side_effect=subprocess.TimeoutExpired('private-command', 25)), \
                patch.object(self.active, 'assign_unassigned_items', side_effect=scan):
            result = self.module.report()
        self.assertEqual(result['error_code'], 'gitlab-timeout')
        self.assertEqual([p['code'] for p in result['problems']], ['queue-scan-failed', 'author-email-unavailable'])
        self.assertNotIn('private-command', json.dumps(result))

    def test_cli_failure_outputs_json_only_and_discards_raw_glab_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'glab').write_text('#!/bin/sh\nprintf "private-token HTTP 403\\n" >&2\nexit 1\n')
            (root / 'glab').chmod(0o755)
            (root / 'config.json').write_text(json.dumps({'skills': {'entries': {'gitlab-agent': {'config': {'owner': 'owner'}}}}}))
            env = {**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH'], 'OPENCLAW_CONFIG_PATH': str(root / 'config.json')}
            for name in ['list-active-items.py', 'work-queue-problems.py']:
                result = subprocess.run(['python3', str(DIRECTORY / name)], env=env, capture_output=True, text=True)
                value = json.loads(result.stdout)
                self.assertEqual(result.stderr, '')
                self.assertNotIn('private-token', result.stdout)
                if name == 'list-active-items.py':
                    self.assertEqual(value, [])
                    self.assertEqual(result.returncode, 69)
                else:
                    self.assertEqual(value['error_code'], 'gitlab-permission')
                    self.assertEqual(value['problems'][0]['code'], 'discovery-failed')

    def test_empty_problems_and_scan_failures_are_json_without_stderr(self):
        for result, error in [({'problems': []}, None), (None, ValueError('private-token'))]:
            out, err = io.StringIO(), io.StringIO()
            with patch.object(self.module, 'report', return_value=result, side_effect=error), redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(self.module.main(), 0)
            self.assertIsInstance(json.loads(out.getvalue())['problems'], list)
            self.assertEqual(err.getvalue(), '')
            self.assertNotIn('private-token', out.getvalue())


if __name__ == '__main__':
    unittest.main()
