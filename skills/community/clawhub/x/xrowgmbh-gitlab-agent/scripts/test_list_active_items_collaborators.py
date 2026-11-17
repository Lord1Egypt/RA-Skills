#!/usr/bin/env python3
"""Controlled API tests for collaborator assignment; no live GitLab writes."""

from __future__ import annotations

import fcntl
import importlib.util
import io
import json
import multiprocessing
import os
import subprocess
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("list_active_items_collaborators", SCRIPT_DIR / "list-active-items.py")
assert spec and spec.loader
active = importlib.util.module_from_spec(spec)
spec.loader.exec_module(active)

AGENT = "eugene-harold-krabs"
PROJECT = "xrow-public/helm-openclaw"


def candidate(iid=7, *, author_id=88, author_name="alice"):
    return {
        "project_id": 22,
        "iid": iid,
        "issue_type": "issue",
        "state": "opened",
        "title": "work",
        "web_url": f"https://gitlab.com/{PROJECT}/-/work_items/{iid}",
        "author": {"id": author_id, "username": author_name},
        "assignees": [],
        "labels": [],
        "updated_at": "2026-10-20T00:00:00.000Z",
        "user_notes_count": 0,
    }


def assigned(item):
    return {**item, "assignees": [{"username": AGENT}]}


def hold_assignment_lock(path, ready, release):
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        ready.send(True)
        release.recv()
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


class EmailDomainTests(unittest.TestCase):
    def test_only_valid_primary_or_public_email_can_match(self):
        accepted = [
            {"email": "alice@XROW.DE"},
            {"public_email": "alice@xrow.de"},
            {"email": "hidden@elsewhere.test", "public_email": "alice@xrow.de"},
            {"email": "alice@xrow.de", "public_email": "bad value"},
        ]
        rejected = [
            {"commit_email": "alice@xrow.de"},
            {"email": "alice@xrow.de.attacker.test"},
            {"public_email": "alice@sub.xrow.de"},
            {"email": "bad value", "public_email": "", "commit_email": "alice@xrow.de"},
            {"email": "a..b@xrow.de"},
            {"email": "a\\b@xrow.de"},
            {"username": "xrow.de", "name": "alice@xrow.de"},
        ]
        for profile in accepted:
            with self.subTest(profile=profile):
                self.assertTrue(active.user_matches_domain(profile, "xrow.de"))
        for profile in rejected:
            with self.subTest(profile=profile):
                self.assertFalse(active.user_matches_domain(profile, "xrow.de"))

    def test_selector_domain_validation(self):
        for invalid in ("", "xrow", ".xrow.de", "xrow..de", "-xrow.de", "xrow.de."):
            self.assertFalse(active.valid_domain(invalid))
        self.assertTrue(active.valid_domain("XROW.DE"))

    def test_explicit_user_and_group_resolution_does_not_search_domain(self):
        def pages(endpoint):
            if endpoint == "users?username=alice":
                return [{"username": "alice"}]
            if endpoint == "groups?search=alice":
                return []
            if endpoint == "users?username=team":
                return []
            if endpoint == "groups?search=team":
                return [{"id": 9, "path": "team"}]
            if endpoint == "groups/9/members/all":
                return [{"username": "bob"}]
            self.fail(f"unexpected endpoint: {endpoint}")
        with patch.object(active, "paginated", side_effect=pages) as fetch:
            self.assertEqual(active.accepted_usernames(["alice", "team", "@xrow.de"]), {"alice", "bob"})
        self.assertNotIn("search=xrow.de", str(fetch.call_args_list))


class AssignmentTests(unittest.TestCase):
    def run_assignment(self, items, profiles, *, selectors=None, explicit=None, states=None, member=True, write_error=False):
        selectors = selectors if selectors is not None else ["@xrow.de"]
        explicit = explicit if explicit is not None else set()
        states = states or {}
        reads = []
        issue_reads = {}

        def api(endpoint):
            reads.append(endpoint)
            if endpoint.startswith("users/"):
                user_id = int(endpoint.split("/")[1])
                value = profiles.get(user_id)
                if value is None:
                    raise subprocess.CalledProcessError(404, "glab")
                return {"id": user_id, **value}
            if "/issues/" in endpoint:
                iid = int(endpoint.rsplit("/", 1)[1])
                issue = next(item for item in items if item["iid"] == iid)
                count = issue_reads.get(iid, 0)
                issue_reads[iid] = count + 1
                return states.get((iid, count), issue if count == 0 else assigned(issue))
            self.fail(f"unexpected API endpoint: {endpoint}")

        def write(command, **_kwargs):
            if write_error:
                raise subprocess.CalledProcessError(502, command)
            iid = int(command[-1].rsplit("/", 1)[1])
            issue = next(item for item in items if item["iid"] == iid)
            return subprocess.CompletedProcess(command, 0, stdout=json.dumps(assigned(issue)))

        with patch.object(active, "configured_accept_entries", return_value=selectors), patch.object(
            active, "accepted_usernames", return_value=explicit
        ), patch.object(active, "assignment_candidates", return_value=items), patch.object(
            active, "owner_created_membership", return_value=member
        ), patch.object(active, "synchronize_forbidden", return_value=[]), patch.object(
            active, "api_json", side_effect=api
        ), patch.object(active.subprocess, "run", side_effect=write) as writer:
            errors = io.StringIO()
            with redirect_stderr(errors):
                result = active.assign_unassigned_items(333, AGENT, "xrow", {})
        return result, reads, writer.call_args_list, errors.getvalue()

    def test_domain_assignment_uses_author_id_and_caches_profile(self):
        items = [candidate(7), candidate(8)]
        result, reads, writes, errors = self.run_assignment(
            items, {88: {"username": "alice", "public_email": "alice@XROW.DE"}}
        )
        self.assertEqual([item["iid"] for item in result], [7, 8])
        self.assertEqual(reads.count("users/88"), 1)
        self.assertEqual(len(writes), 2)
        self.assertTrue(all("assignee_ids=333" in call.args[0] for call in writes))
        self.assertNotIn("search=", str(reads))
        self.assertEqual(errors, "")

    def test_primary_email_or_explicit_rule_can_assign(self):
        for profiles, selectors, explicit in (
            ({88: {"email": "alice@xrow.de", "public_email": "bad value"}}, ["@xrow.de"], set()),
            ({}, ["alice"], {"alice"}),
            ({}, ["team"], {"alice"}),
        ):
            with self.subTest(selectors=selectors):
                result, reads, writes, _ = self.run_assignment(
                    [candidate()], profiles, selectors=selectors, explicit=explicit
                )
                self.assertEqual(len(result), 1)
                self.assertEqual(len(writes), 1)
                if explicit:
                    self.assertNotIn("users/88", reads)

    def test_unmatched_or_failed_profile_never_assigns(self):
        for profiles in (
            {88: {"commit_email": "alice@xrow.de", "public_email": ""}},
            {88: {"email": "alice@xrow.de.attacker.test"}},
            {},
        ):
            with self.subTest(profiles=profiles):
                result, _, writes, _ = self.run_assignment([candidate()], profiles)
                self.assertEqual(result, [])
                self.assertEqual(writes, [])

    def test_project_denial_or_stale_issue_state_prevents_write(self):
        issue = candidate()
        for member, state in (
            (False, None),
            (True, {**issue, "state": "closed"}),
            (True, {**issue, "labels": ["workflow::paused"]}),
            (True, {**issue, "assignees": [{"username": "other"}]}),
        ):
            with self.subTest(member=member, state=state):
                states = {(7, 0): state} if state else {}
                result, _, writes, _ = self.run_assignment(
                    [issue], {88: {"public_email": "alice@xrow.de"}}, member=member, states=states
                )
                self.assertEqual(result, [])
                self.assertEqual(writes, [])

    def test_unconfirmed_or_ambiguous_write_is_not_blindly_retried(self):
        issue = candidate()
        result, _, writes, errors = self.run_assignment(
            [issue], {88: {"public_email": "alice@xrow.de"}},
            states={(7, 1): {**issue, "assignees": [{"username": "other"}]}},
            write_error=True,
        )
        self.assertEqual(result, [])
        self.assertEqual(len(writes), 1)
        self.assertIn("ambiguous", errors)
        self.assertIn("unconfirmed", errors)

    def test_ambiguous_write_confirmed_by_fresh_read_is_returned(self):
        result, _, writes, errors = self.run_assignment(
            [candidate()], {88: {"public_email": "alice@xrow.de"}}, write_error=True
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(len(writes), 1)
        self.assertIn("ambiguous", errors)

    def test_assignment_holds_and_releases_local_lock(self):
        with patch.object(active, "configured_accept_entries", return_value=["alice"]), patch.object(
            active, "accepted_usernames", return_value={"alice"}
        ), patch.object(active, "assignment_candidates", return_value=[]), patch.object(
            fcntl, "flock"
        ) as lock:
            self.assertEqual(active.assign_unassigned_items(333, AGENT, "xrow", {}), [])
        self.assertEqual([call.args[1] for call in lock.call_args_list], [fcntl.LOCK_EX, fcntl.LOCK_UN])

    def test_parallel_run_waits_for_local_assignment_lock(self):
        context = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / f"gitlab-agent-assign-{os.getuid()}.lock")
            ready_parent, ready_child = context.Pipe()
            release_parent, release_child = context.Pipe()
            holder = context.Process(target=hold_assignment_lock, args=(path, ready_child, release_child))
            holder.start()
            try:
                self.assertTrue(ready_parent.poll(5))
                self.assertTrue(ready_parent.recv())
                finished = threading.Event()
                def run():
                    try:
                        active.assign_unassigned_items(333, AGENT, "xrow", {})
                    finally:
                        finished.set()
                with patch("tempfile.gettempdir", return_value=directory), patch.object(
                    active, "configured_accept_entries", return_value=["alice"]
                ), patch.object(active, "accepted_usernames", return_value={"alice"}), patch.object(
                    active, "assignment_candidates", return_value=[]
                ):
                    contender = threading.Thread(target=run, daemon=True)
                    contender.start()
                    self.assertFalse(finished.wait(0.15))
                    release_parent.send(True)
                    self.assertTrue(finished.wait(5))
                    contender.join(5)
            finally:
                if holder.is_alive():
                    try:
                        release_parent.send(True)
                    except (BrokenPipeError, OSError):
                        pass
                holder.join(5)
                if holder.is_alive():
                    holder.terminate()
                    holder.join(5)
            self.assertEqual(holder.exitcode, 0)


class CandidateTests(unittest.TestCase):
    def test_active_owner_created_project_only_and_deduplicates_issues(self):
        issue = candidate()
        seen = []
        def pages(endpoint):
            seen.append(endpoint)
            if endpoint == "projects?membership=true&simple=true":
                return [
                    {"id": 22, "path_with_namespace": PROJECT},
                    {"id": 23, "path_with_namespace": "untrusted/project"},
                    {"id": 24, "path_with_namespace": "archived/project"},
                ]
            if endpoint.startswith("projects/22/issues?"):
                return [issue, issue, {**candidate(8), "issue_type": "incident"}, {**candidate(9), "issue_type": "task"}]
            self.fail(f"unexpected candidate query: {endpoint}")
        with patch.object(active, "paginated", side_effect=pages), patch.object(
            active, "project_is_active", side_effect=lambda project_id, _cache: project_id != 24
        ), patch.object(
            active, "owner_created_membership", side_effect=lambda path, *_: path == PROJECT
        ):
            result = active.assignment_candidates(333, AGENT, "xrow", {})
        self.assertEqual([item["iid"] for item in result], [7, 9])
        self.assertEqual(sum("projects/22/issues?" in call for call in seen), 1)
        self.assertTrue(any("scope=all" in call for call in seen))
        self.assertFalse(any("projects/23/issues?" in call for call in seen))


    def test_candidate_url_must_match_member_project(self):
        bad = {**candidate(), "web_url": "https://gitlab.com/other/project/-/issues/7"}
        def pages(endpoint):
            if endpoint == "projects?membership=true&simple=true":
                return [{"id": 22, "path_with_namespace": PROJECT}]
            if endpoint.startswith("projects/22/issues?"):
                return [bad]
            self.fail(f"unexpected page: {endpoint}")
        with patch.object(active, "paginated", side_effect=pages), patch.object(
            active, "project_is_active", return_value=True
        ), patch.object(active, "owner_created_membership", return_value=True):
            with self.assertRaisesRegex(ValueError, "project path is inconsistent"):
                active.assignment_candidates(333, AGENT, "xrow", {})

    def test_invalid_collaborator_flow_does_not_hide_assigned_work_or_incident(self):
        assigned_issue = assigned(candidate(7))
        incident = {**assigned(candidate(8)), "issue_type": "incident"}
        def pages(endpoint):
            if endpoint == "issues?state=opened&scope=assigned_to_me":
                return [assigned_issue]
            if endpoint == "merge_requests?state=opened&scope=assigned_to_me":
                return []
            self.fail(f"unexpected page: {endpoint}")
        with patch.object(active.shutil, "which", return_value="/usr/bin/glab"), patch.object(
            active, "api_json", return_value={"id": 333, "username": AGENT}
        ), patch.object(active, "configured_owner", return_value="xrow"), patch.object(
            active, "unassigned_incidents", return_value=[incident]
        ), patch.object(active, "adopt_incident", return_value=incident), patch.object(
            active, "paginated", side_effect=pages
        ), patch.object(active, "project_is_active", return_value=True), patch.object(
            active, "assign_unassigned_items", side_effect=ValueError("invalid selector")
        ), patch.object(
            active, "permitted_items", side_effect=lambda records, *_: [active.normalized(item, kind) for item, kind in records]
        ), patch.object(active, "root_cause_flags", side_effect=lambda rows: [False] * len(rows)):
            output, errors = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(active.main(), 0)
        self.assertEqual({row["iid"] for row in json.loads(output.getvalue())}, {7, 8})
        self.assertIn("collaborator assignment unavailable", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
