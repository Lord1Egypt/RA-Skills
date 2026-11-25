#!/usr/bin/env python3
"""Regression tests for deterministic reviewer selection."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parent / "select-reviewer.py"
SPEC = importlib.util.spec_from_file_location("select_reviewer", SCRIPT)
assert SPEC and SPEC.loader
reviewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)


ME = {"id": 99, "username": "robot"}
PROJECT = {"id": 1, "default_branch": "main"}
MR = {
    "iid": 7,
    "state": "opened",
    "sha": "abc",
    "target_branch": "main",
    "author": {"id": 99, "username": "robot"},
    "assignees": [{"id": 99, "username": "robot"}],
    "reviewers": [{"id": 77, "username": "existing"}],
    "head_pipeline": {"status": "success", "sha": "abc"},
    "diverged_commits_count": 0,
    "rebase_in_progress": False,
    "has_conflicts": False,
}
MEMBERS = [
    {
        "id": 99,
        "username": "robot",
        "access_level": 30,
        "state": "active",
        "locked": False,
    },
    {
        "id": 2,
        "username": "andyxrow",
        "access_level": 40,
        "state": "active",
        "locked": False,
    },
    {
        "id": 3,
        "username": "xrow",
        "access_level": 50,
        "state": "active",
        "locked": False,
    },
]


def linked(author_id: int, username: str, iid: int = 19) -> dict[str, object]:
    return {"id": iid, "iid": iid, "author": {"id": author_id, "username": username}}


class ReviewerSelectionTests(unittest.TestCase):
    def run_selection(
        self,
        *,
        linked_items=None,
        members=None,
        agents=False,
        agents_markdown="| reviewers | [xrow](https://gitlab.com/xrow) |\n",
        bot_ids=None,
        changed=False,
        ignored=None,
        self_review=False,
        optional=False,
        approval_changed=False,
        approval_fails=False,
        can_merge=True,
        can_approve=True,
        mr_overrides=None,
        fresh_members=None,
        fresh_member=None,
        mr_change=None,
        post_approval_mr_change=None,
        commits=None,
        fresh_commits=None,
        user_emails=None,
        receipt_overrides=None,
    ):
        linked_items = [] if linked_items is None else linked_items
        members = MEMBERS if members is None else members
        selected_mr = {
            **MR,
            **({
                "reviewers": [],
                "draft": False,
                "merge_status": "can_be_merged",
                "detailed_merge_status": "mergeable",
                "blocking_discussions_resolved": True,
                "head_pipeline": {"status": "success", "sha": "abc"},
            } if self_review else {}),
        }
        selected_mr.update(mr_overrides or {})
        fresh_mr = {**selected_mr, "sha": "changed"} if changed else selected_mr
        fresh_mr = {**fresh_mr, **(mr_change or {})}
        bot_ids = set() if bot_ids is None else set(bot_ids)
        ignored = set() if ignored is None else set(ignored)
        commits = [{"id": "commit-one", "committer_email": "xrow@example.com"}] if commits is None else commits
        user_emails = {3: "xrow@example.com"} if user_emails is None else user_emails

        def object_for(endpoint, _description):
            if endpoint == "user":
                return ME
            if endpoint == "projects/example%2Fproject":
                return PROJECT
            if endpoint == "projects/example%2Fproject/merge_requests/7":
                return selected_mr
            if "/members/all/" in endpoint:
                return fresh_member or next(
                    member for member in members
                    if member["id"] == int(endpoint.rsplit("/", 1)[1])
                )
            if endpoint.startswith("users/"):
                user_id = int(endpoint.removeprefix("users/"))
                return {"id": user_id, "bot": user_id in bot_ids,
                        "public_email": user_emails.get(user_id, "")}
            raise AssertionError(endpoint)

        membership_calls = 0
        commit_calls = 0

        def pages(endpoint, _description):
            nonlocal membership_calls, commit_calls
            if endpoint.endswith("/commits"):
                commit_calls += 1
                return fresh_commits if commit_calls > 1 and fresh_commits is not None else commits
            if "/members/all" in endpoint:
                membership_calls += 1
                if membership_calls > 1 and fresh_members is not None:
                    return fresh_members
                return members
            if "/closes_issues" in endpoint:
                return linked_items
            if "/repository/tree" in endpoint:
                return [{"path": "AGENTS.md"}] if agents else []
            raise AssertionError(endpoint)

        object_calls = {"mr": 0}
        persisted_reviewers = selected_mr["reviewers"]
        approval_performed = False

        def objects(endpoint, description):
            if endpoint.split("?", 1)[0] == "projects/example%2Fproject/merge_requests/7":
                self.assertIn("include_rebase_in_progress=true", endpoint)
                self.assertIn("include_diverged_commits_count=true", endpoint)
                if description == "reviewer assignment receipt":
                    return {**fresh_mr, "reviewers": persisted_reviewers,
                            **(receipt_overrides or {})}
                object_calls["mr"] += 1
                if approval_performed and post_approval_mr_change is not None:
                    return {**fresh_mr, **post_approval_mr_change}
                return fresh_mr if object_calls["mr"] > 1 else selected_mr
            return object_for(endpoint, description)

        approval_state_calls = 0

        def api_text(endpoint):
            nonlocal approval_state_calls
            if endpoint.endswith("/repository/branches/main"):
                return json.dumps({"name": "main", "protected": True})
            if endpoint.endswith("/protected_branches/main"):
                return json.dumps({"name": "main", "merge_access_levels": (
                    [{"access_level": 30}] if can_merge else []
                )})
            if endpoint.endswith("/approvals"):
                return json.dumps({
                    "user_can_approve": can_approve,
                    "approvals_required": 0 if optional else 1,
                    "approvals_left": 0 if optional else 1,
                })
            if endpoint.endswith("/approval_state"):
                approval_state_calls += 1
                required = 0 if optional and not (
                    approval_changed and approval_state_calls > 1
                ) else 1
                return json.dumps({"rules": [{"approvals_required": required}]})
            return agents_markdown

        def run_command(args, **_kwargs):
            nonlocal persisted_reviewers, approval_performed
            if "input" in _kwargs:
                ids = json.loads(_kwargs["input"])["reviewer_ids"]
                identities = {m["id"]: m for m in [*members, *selected_mr["reviewers"]]}
                persisted_reviewers = [identities[i] for i in ids]
            if approval_fails and any("/approve" in part for part in args):
                raise subprocess.CalledProcessError(403, args)
            if any("/approve" in part for part in args):
                approval_performed = True
            return Mock(stdout='{"state":"merged"}')

        command = Mock(side_effect=run_command)
        self.last_command = command
        stdout = io.StringIO()
        with patch.object(reviewer, "ignored_reviewers", return_value=ignored), patch.object(
            reviewer.shutil, "which", return_value="/usr/bin/glab"
        ), patch.object(
            reviewer, "api_object", side_effect=objects
        ), patch.object(reviewer, "api_pages", side_effect=pages), patch.object(
            reviewer,
            "api_text",
            side_effect=api_text,
        ), patch.object(reviewer.subprocess, "run", command), redirect_stdout(stdout):
            reviewer.main(
                ["example/project", "7"]
            )
        return json.loads(stdout.getvalue()), command

    def test_http_success_without_persisted_candidate_fails_closed(self):
        errors = io.StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit) as error:
            self.run_selection(receipt_overrides={"reviewers": MR["reviewers"]})
        self.assertEqual(error.exception.code, 78)
        self.assertIn("did not confirm", errors.getvalue())
        self.last_command.assert_called_once()

    def test_incomplete_or_dropped_existing_reviewers_never_approve(self):
        for reviewers in (None, "invalid", [{"id": 99}], [], [ME]):
            with self.subTest(reviewers=reviewers), redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit):
                self.run_selection(self_review=True, optional=True,
                                   mr_overrides={"reviewers": MR["reviewers"]},
                                   receipt_overrides={"reviewers": reviewers})
            self.last_command.assert_called_once()

    def test_unpersisted_self_reviewer_cannot_approve_or_merge(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(self_review=True, optional=True,
                               receipt_overrides={"reviewers": []})
        self.last_command.assert_called_once()

    def test_changed_source_after_write_cannot_approve_or_merge(self):
        for changed in ({"sha": "new-source"}, {"target_branch": "other"}, {"iid": 8}):
            with self.subTest(changed=changed), redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit):
                self.run_selection(self_review=True, optional=True,
                                   receipt_overrides=changed)
            self.last_command.assert_called_once()

    def test_extra_concurrent_reviewer_is_preserved(self):
        result, command = self.run_selection(receipt_overrides={"reviewers": [
            *MR["reviewers"], MEMBERS[1], {"id": 88, "username": "concurrent"}]})
        self.assertTrue(result["applied"])
        command.assert_called_once()

    def assert_dod_failure(self, expected, **arguments):
        errors = io.StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit) as error:
            self.run_selection(**arguments)
        self.assertEqual(error.exception.code, 78)
        self.assertIn("Definition of Done not met", errors.getvalue())
        self.assertIn(expected, errors.getvalue())
        self.last_command.assert_not_called()
        return errors.getvalue()

    def merged_fixture(self):
        head, merged, target = "a" * 40, "b" * 40, "c" * 40
        mr = {**MR, "project_id": 1, "sha": head,
              "head_pipeline": {"status": "success", "sha": merged, "project_id": 1,
                                "source": "merge_request_event", "ref": "refs/merge-requests/7/merge"}}
        return mr, {"id": merged, "parent_ids": [target, head]}, {"name": "main", "commit": {"id": target}}

    def test_current_merged_result_qualifies_without_weakening_rebase_gates(self):
        mr, commit, branch = self.merged_fixture()
        with patch.object(reviewer, "api_object", side_effect=[commit, branch]) as api:
            reviewer.require_definition_of_done(mr)
        self.assertEqual(api.call_count, 2)
        self.assertTrue(api.call_args_list[0].args[0].endswith("/repository/commits/" + "b" * 40))
        self.assertTrue(api.call_args_list[1].args[0].endswith("/repository/branches/main"))
        with patch.object(reviewer, "api_object", side_effect=[commit, branch]), \
                redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            reviewer.require_definition_of_done({**mr, "diverged_commits_count": 1})
        ready = {**mr, "draft": False, "merge_status": "can_be_merged",
                 "detailed_merge_status": "mergeable", "blocking_discussions_resolved": True}
        with patch.object(reviewer, "api_object", side_effect=[commit, branch]):
            self.assertTrue(reviewer.merge_ready(ready))

    def test_merged_result_metadata_must_identify_this_project_and_mr(self):
        mr, _, _ = self.merged_fixture()
        for key, value in [("project_id", 2), ("project_id", True), ("source", "push"),
                           ("ref", "refs/merge-requests/8/merge"), ("ref", "refs/merge-requests/7/head"),
                           ("sha", "invalid"), ("status", "running")]:
            with self.subTest(key=key, value=value), patch.object(reviewer, "api_object") as api:
                self.assertFalse(reviewer.pipeline_matches_head({**mr, "head_pipeline": {**mr['head_pipeline'], key: value}}))
                api.assert_not_called()

    def test_wrong_missing_or_stale_merge_parents_fail_closed(self):
        mr, commit, branch = self.merged_fixture()
        for wrong_commit, wrong_branch in [
            ({**commit, "id": "d" * 40}, branch),
            ({**commit, "parent_ids": ["d" * 40, mr['sha']]}, branch),
            ({**commit, "parent_ids": [branch['commit']['id'], "d" * 40]}, branch),
            ({**commit, "parent_ids": [mr['sha'], branch['commit']['id']]}, branch),
            ({**commit, "parent_ids": []}, branch),
            ({**commit, "parent_ids": [branch['commit']['id'], mr['sha'], 'd' * 40]}, branch),
            ({**commit, "parent_ids": ['', mr['sha']]}, {**branch, "commit": {"id": ''}}),
            (commit, {}), (commit, {**branch, "name": "other"}),
            (commit, {**branch, "commit": {"id": "d" * 40}}),
        ]:
            with self.subTest(commit=wrong_commit, branch=wrong_branch), \
                    patch.object(reviewer, "api_object", side_effect=[wrong_commit, wrong_branch]):
                self.assertFalse(reviewer.pipeline_matches_head(mr))

    def test_merge_proof_is_refreshed_and_api_denial_never_qualifies(self):
        mr, commit, branch = self.merged_fixture()
        with patch.object(reviewer, "api_object", side_effect=[commit, branch, commit,
                {**branch, "commit": {"id": "d" * 40}}]) as api:
            self.assertTrue(reviewer.pipeline_matches_head(mr))
            self.assertFalse(reviewer.pipeline_matches_head(mr))
            self.assertEqual(api.call_count, 4)
        with patch.object(reviewer, "api_object", side_effect=SystemExit(78)), self.assertRaises(SystemExit):
            reviewer.pipeline_matches_head(mr)

    def test_latest_pipeline_must_succeed_before_any_reviewer_assignment(self):
        pipelines = [None, {}, {"status": "success", "sha": "old-head"}]
        pipelines += [
            {"status": status, "sha": "abc"}
            for status in ("failed", "canceled", "skipped", "running", "pending", "manual")
        ]
        for members in (MEMBERS, [{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]]):
            for pipeline in pipelines:
                with self.subTest(agent_level=members[0]["access_level"], pipeline=pipeline):
                    self.assert_dod_failure(
                        "latest pipeline", members=members,
                        mr_overrides={"head_pipeline": pipeline},
                    )

    def test_rebase_requirement_or_unavailable_state_prevents_assignment(self):
        for changes, expected in (
            ({"diverged_commits_count": 1}, "rebase required"),
            ({"detailed_merge_status": "need_rebase"}, "rebase required"),
            ({"detailed_merge_status": "conflict"}, "rebase required"),
            ({"has_conflicts": True}, "rebase required"),
            ({"merge_error": "Rebase failed. Please rebase locally"}, "rebase required"),
            ({"rebase_in_progress": True}, "rebase is still in progress"),
            ({"rebase_in_progress": None}, "rebase status is unavailable"),
            ({"diverged_commits_count": None}, "cannot determine whether a rebase is needed"),
            ({"diverged_commits_count": -1}, "cannot determine whether a rebase is needed"),
            ({"diverged_commits_count": True}, "cannot determine whether a rebase is needed"),
        ):
            with self.subTest(changes=changes):
                self.assert_dod_failure(expected, mr_overrides=changes)

    def test_pipeline_and_rebase_errors_are_reported_together(self):
        errors = self.assert_dod_failure("latest pipeline", mr_overrides={
            "head_pipeline": {"status": "failed", "sha": "abc"},
            "diverged_commits_count": 2,
        })
        self.assertIn("status: failed", errors)
        self.assertIn("rebase required", errors)

    def test_dod_is_rechecked_before_human_self_and_fallback_assignment(self):
        for arguments in (
            {},
            {"members": [{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]]},
            {"members": [MEMBERS[0], MEMBERS[2]], "mr_overrides": {"author": MEMBERS[2]}},
        ):
            for changes, expected in (
                ({"head_pipeline": {"status": "running", "sha": "abc"}}, "latest pipeline"),
                ({"diverged_commits_count": 1}, "rebase required"),
                ({"rebase_in_progress": True}, "rebase is still in progress"),
            ):
                with self.subTest(arguments=arguments, changes=changes):
                    self.assert_dod_failure(expected, mr_change=changes, **arguments)

    def test_dod_change_after_approval_prevents_merge(self):
        for changes, expected in (
            ({"head_pipeline": {"status": "failed", "sha": "abc"}}, "latest pipeline"),
            ({"diverged_commits_count": 1}, "rebase required"),
        ):
            with self.subTest(changes=changes):
                errors = io.StringIO()
                with redirect_stderr(errors), self.assertRaises(SystemExit):
                    self.run_selection(
                        self_review=True, optional=True, post_approval_mr_change=changes,
                    )
                self.assertIn(expected, errors.getvalue())
                calls = self.last_command.call_args_list
                self.assertEqual(len(calls), 2)
                self.assertTrue(calls[1].args[0][4].endswith("/approve"))
                self.assertFalse(any(call.args[0][4].endswith("/merge") for call in calls))

    def test_removed_apply_option_is_rejected_before_gitlab_access(self):
        with patch.object(reviewer, "api_object") as api, redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                reviewer.main(["--apply", "example/project", "7"])
        self.assertEqual(error.exception.code, 2)
        api.assert_not_called()

    def test_prefers_unique_linked_work_item_author(self):
        result, _command = self.run_selection(
            linked_items=[linked(2, "andyxrow")], agents=True
        )
        self.assertEqual(result["reviewer"]["username"], "andyxrow")
        self.assertEqual(result["rule"], "linked-work-item-author")
        self.assertTrue(result["applied"])
        _command.assert_called_once()
        self.assertEqual(json.loads(_command.call_args.kwargs["input"]),
                         {"reviewer_ids": [2, 77]})

    def test_prefers_configured_reviewer_without_linked_author(self):
        result, _command = self.run_selection(agents=True)
        self.assertEqual(result["reviewer"]["username"], "xrow")
        self.assertEqual(result["rule"], "configured-reviewer")

    def test_falls_back_to_maintainer_then_owner(self):
        result, _command = self.run_selection()
        self.assertEqual(result["reviewer"]["username"], "andyxrow")
        self.assertEqual(result["rule"], "maintainer-fallback")
        owner_only = [MEMBERS[0], MEMBERS[2]]
        result, _command = self.run_selection(members=owner_only)
        self.assertEqual(result["reviewer"]["username"], "xrow")
        self.assertEqual(result["rule"], "owner-fallback")

    def test_maintainer_or_owner_agent_is_preferred_reviewer(self):
        for level in (40, 50):
            for arguments in (
                {},
                {"linked_items": [linked(2, "andyxrow")], "agents": True},
                {"agents": True},
                {"linked_items": [linked(2, "andyxrow"), linked(3, "xrow", 20)]},
            ):
                with self.subTest(level=level, arguments=arguments):
                    result, command = self.run_selection(
                        members=[{**MEMBERS[0], "access_level": level}, *MEMBERS[1:]],
                        bot_ids={99}, **arguments,
                    )
                    self.assertEqual(result["reviewer"]["id"], ME["id"])
                    self.assertEqual(result["rule"], "maintainer-self-review")
                    self.assertFalse(result["self_merge"])
                    self.assertTrue(result["applied"])
                    command.assert_called_once()
                    self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                                     {"reviewer_ids": [77, 99]})

    def test_maintainer_apply_preserves_existing_reviewers_without_approval(self):
        result, command = self.run_selection(
            members=[{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]],
            mr_overrides={"author": MEMBERS[2]}, bot_ids={99},
        )
        self.assertTrue(result["applied"])
        self.assertFalse(result["self_merge"])
        self.assertFalse(result["merged"])
        self.assertEqual(command.call_count, 1)
        self.assertEqual(command.call_args.args[0][3], "PUT")
        self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                         {"reviewer_ids": [77, 99]})

    def test_maintainer_nomination_preserves_approval_and_merge_gates(self):
        for arguments in (
            {"optional": False},
            {"optional": True, "can_approve": False},
            {"optional": True, "can_merge": False},
            {"optional": True, "mr_overrides": {"draft": True}},
            {"optional": True, "mr_overrides": {"blocking_discussions_resolved": False}},
        ):
            with self.subTest(arguments=arguments):
                result, command = self.run_selection(
                    members=[{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]],
                    self_review=True, **arguments,
                )
                self.assertEqual(result["rule"], "maintainer-self-review")
                self.assertFalse(result["self_merge"])
                self.assertFalse(result["merged"])
                self.assertEqual(command.call_count, 1)
                self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                                 {"reviewer_ids": [99]})

    def test_maintainer_optional_approval_can_still_self_merge(self):
        result, command = self.run_selection(
            members=[{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]],
            self_review=True, optional=True, bot_ids={99},
        )
        self.assertEqual(result["rule"], "optional-approval-self-merge")
        self.assertTrue(result["self_merge"])
        self.assertTrue(result["merged"])
        self.assertEqual(command.call_count, 3)

    def test_inactive_locked_or_ignored_maintainer_uses_human_reviewer(self):
        for changes, ignored in (
            ({"state": "blocked"}, set()),
            ({"locked": True}, set()),
            ({}, {"robot"}),
        ):
            with self.subTest(changes=changes, ignored=ignored):
                result, command = self.run_selection(
                    members=[{**MEMBERS[0], "access_level": 40, **changes}, *MEMBERS[1:]],
                    ignored=ignored, self_review=True, optional=True,
                )
                self.assertEqual(result["reviewer"]["username"], "andyxrow")
                self.assertFalse(result["self_merge"])
                self.assertTrue(result["applied"])
                command.assert_called_once()

    def test_maintainer_apply_revalidates_role_account_and_merge_request(self):
        for arguments in (
            {"fresh_member": {**MEMBERS[0], "access_level": 30}},
            {"fresh_member": {**MEMBERS[0], "access_level": 40, "locked": True}},
            {"fresh_member": {**MEMBERS[0], "access_level": 40, "state": "blocked"}},
            {"changed": True},
        ):
            with self.subTest(arguments=arguments), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.run_selection(
                    members=[{**MEMBERS[0], "access_level": 40}, *MEMBERS[1:]],
                    **arguments,
                )
            self.last_command.assert_not_called()

    def test_excludes_bots_and_service_accounts_from_every_rule(self):
        service_account = {
            "id": 4,
            "username": "sa-xrow-public",
            "access_level": 40,
            "state": "active",
            "locked": False,
        }
        result, _command = self.run_selection(
            members=[MEMBERS[0], service_account, MEMBERS[2]],
            linked_items=[linked(4, "sa-xrow-public")],
            agents=True,
            agents_markdown=(
                "| reviewers | [sa-xrow-public](https://gitlab.com/sa-xrow-public), "
                "[xrow](https://gitlab.com/xrow) |\n"
            ),
            bot_ids={4},
        )
        self.assertEqual(result["reviewer"]["username"], "xrow")
        self.assertEqual(result["rule"], "configured-reviewer")
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(
                members=[MEMBERS[0], service_account],
                mr_overrides={"author": service_account},
                bot_ids={4},
            )

    def test_fails_on_ambiguous_authors_or_incomplete_membership(self):
        cases = [
            {
                "linked_items": [linked(2, "andyxrow"), linked(3, "xrow", 20)],
            },
            {
                "members": [
                    {
                        "id": 2,
                        "username": "andyxrow",
                        "access_level": 40,
                        "state": "active",
                    }
                ]
            },
        ]
        for arguments in cases:
            with (
                self.subTest(arguments=arguments),
                redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                self.run_selection(**arguments)

    def test_ignored_linked_author_uses_configured_reviewer(self):
        result, _command = self.run_selection(
            linked_items=[linked(2, "andyxrow")],
            agents=True,
            ignored={"andyxrow"},
        )
        self.assertEqual(result["reviewer"]["username"], "xrow")
        self.assertEqual(result["rule"], "configured-reviewer")

    def test_ignored_configured_reviewer_uses_fallback(self):
        result, _command = self.run_selection(agents=True, ignored={"xrow"})
        self.assertEqual(result["reviewer"]["username"], "andyxrow")
        self.assertEqual(result["rule"], "maintainer-fallback")

    def test_all_reviewers_including_author_ignored_fails_closed(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(ignored={"robot", "andyxrow", "xrow"})

    # Superseding owner contract: !200#note_4081781371. Only actual committers
    # qualify in the last tier, ordered Owner, Maintainer, then Developer.
    def test_committer_fallback_allows_author_assignee_without_approval(self):
        result, command = self.run_selection(
            members=[MEMBERS[0], MEMBERS[2]],
            mr_overrides={"author": {"id": 3, "username": "xrow"},
                          "assignees": [ME, MEMBERS[2]]},
        )
        self.assertEqual(result["reviewer"]["username"], "xrow")
        self.assertEqual(result["rule"], "merge-request-committer-fallback")
        self.assertTrue(result["committer_fallback"])
        self.assertFalse(result["self_merge"])
        self.assertFalse(result["merged"])
        self.assertIn("independent approval", result["approval_warning"])
        self.assertEqual(command.call_count, 1)
        self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                         {"reviewer_ids": [3, 77]})

    def test_committer_need_not_be_the_mr_author(self):
        developer = {**MEMBERS[1], "access_level": 30}
        result, command = self.run_selection(
            members=[MEMBERS[0], developer],
            commits=[{"id": "one", "committer_email": "andy@example.com"}],
            user_emails={2: "andy@example.com"},
        )
        self.assertEqual(result["reviewer"]["id"], 2)
        self.assertTrue(result["committer_fallback"])
        self.assertTrue(result["applied"])
        command.assert_called_once()
        self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                         {"reviewer_ids": [2, 77]})

    def test_author_without_matching_commit_is_last_resort_nomination(self):
        result, command = self.run_selection(members=[MEMBERS[0], MEMBERS[2]],
            mr_overrides={"author": MEMBERS[2]},
            commits=[{"id": "one", "committer_email": "someone-else@example.com"}])
        self.assertEqual(result["reviewer"]["id"], 3)
        self.assertTrue(result["author_fallback"])
        self.assertFalse(result["committer_fallback"])
        self.assertFalse(result["self_merge"])
        self.assertFalse(result["merged"])
        self.assertIn("independent approval", result["approval_warning"])
        self.assertEqual(command.call_count, 1)
        self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                         {"reviewer_ids": [3, 77]})

    def test_current_agent_author_can_be_nominated_but_not_approved(self):
        result, command = self.run_selection(members=[MEMBERS[0]], bot_ids={99})
        self.assertTrue(result["author_fallback"])
        self.assertFalse(result["self_merge"])
        self.assertFalse(result["merged"])
        self.assertEqual(command.call_count, 1)
        self.assertEqual(json.loads(command.call_args.kwargs["input"]),
                         {"reviewer_ids": [77, 99]})

    def test_author_fallback_revalidates_and_preserves_exclusions(self):
        for extra in ({"fresh_members": MEMBERS},
            {"fresh_members": [MEMBERS[0]]},
            {"fresh_member": {**MEMBERS[2], "locked": True}},
            {"mr_change": {"author": ME}}, {"changed": True},
            {"fresh_commits": [{"id": "changed", "committer_email": "xrow@example.com"}]}):
            with self.subTest(extra=extra), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.run_selection(members=[MEMBERS[0], MEMBERS[2]],
                    mr_overrides={"author": MEMBERS[2]}, commits=[], **extra)
            self.last_command.assert_not_called()

    def test_author_fallback_stops_when_committer_appears(self):
        developer = {**MEMBERS[1], "access_level": 30}
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(members=[MEMBERS[0]],
                fresh_members=[MEMBERS[0], developer],
                commits=[{"id": "one", "committer_email": "andy@example.com"}],
                user_emails={2: "andy@example.com"})
        self.last_command.assert_not_called()

    def test_committer_role_order_owner_then_maintainer_then_developer(self):
        developer = {**MEMBERS[1], "id": 4, "username": "developer", "access_level": 30}
        humans = [MEMBERS[1], MEMBERS[2], developer]
        commits = [{"id": str(m["id"]), "committer_email": m["username"] + "@example.com"}
                   for m in humans]
        emails = {m["id"]: m["username"] + "@example.com" for m in humans}
        for available, expected in ((humans, 3), ([humans[0], developer], 2), ([developer], 4)):
            with self.subTest(expected=expected):
                result, _ = self.run_selection(members=[MEMBERS[0], *available],
                    mr_overrides={"assignees": [ME, *available]},
                    commits=commits, user_emails=emails)
                self.assertEqual(result["reviewer"]["id"], expected)
                self.assertTrue(result["committer_fallback"])

    def test_preferred_reviewers_win_over_committer_fallback(self):
        for arguments in ({"linked_items": [linked(2, "andyxrow")]},
            {"agents": True, "agents_markdown": "| reviewers | [andyxrow](https://gitlab.com/andyxrow) |"}, {}):
            with self.subTest(arguments=arguments):
                result, _ = self.run_selection(
                    mr_overrides={"author": MEMBERS[2]}, **arguments)
                self.assertEqual(result["reviewer"]["id"], 2)
                self.assertFalse(result["committer_fallback"])

    def test_committer_fallback_keeps_account_membership_and_ignore_guards(self):
        for extra in ({"members": [MEMBERS[0]]},
            {"members": [MEMBERS[0], {**MEMBERS[2], "locked": True}]},
            {"members": [MEMBERS[0], {**MEMBERS[2], "state": "blocked"}]},
            {"members": [MEMBERS[0], {**MEMBERS[2], "access_level": 10}]},
            {"bot_ids": {3}}, {"ignored": {"xrow"}}):
            arguments = {"members": [MEMBERS[0], MEMBERS[2]], "mr_overrides": {"author": MEMBERS[2]}, **extra}
            with self.subTest(arguments=arguments), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.run_selection(**arguments)
        result, _ = self.run_selection(members=[MEMBERS[0]],
            commits=[{"id": "one", "committer_email": "robot@example.com"}],
            user_emails={99: "robot@example.com"})
        self.assertTrue(result["author_fallback"])
        self.assertFalse(result["committer_fallback"])

    def test_committer_fallback_revalidates_before_mutating(self):
        for fresh in ({"fresh_member": {**MEMBERS[2], "locked": True}},
            {"fresh_members": [MEMBERS[0]]}, {"fresh_members": MEMBERS},
            {"fresh_members": [MEMBERS[0], {"id": 3}]},
            {"fresh_commits": [{"id": "one", "committer_email": "different@example.com"}]},
            {"mr_change": {"author": MEMBERS[1]}}, {"changed": True}):
            with self.subTest(fresh=fresh), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.run_selection(members=[MEMBERS[0], MEMBERS[2]],
                    mr_overrides={"author": MEMBERS[2]}, **fresh)
            self.last_command.assert_not_called()

    def test_invalid_or_ambiguous_committer_data_fails_closed(self):
        for commits, emails in (([{"id": "one"}], {3: "xrow@example.com"}),
            ([{"id": "one", "committer_email": "xrow@example.com"}], {2: "xrow@example.com", 3: "xrow@example.com"})):
            with self.subTest(commits=commits), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.run_selection(mr_overrides={"assignees": [ME, MEMBERS[1], MEMBERS[2]]}, commits=commits, user_emails=emails)

    def test_reads_nested_and_direct_reviewer_exclusions(self):
        for agent in (
            {"config": {"reviewer": {"ignore": ["xrow", "GitLabDuo"]}}},
            {"reviewer": {"ignore": ["xrow", "GitLabDuo"]}},
        ):
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                config = Path(directory) / "openclaw.json"
                config.write_text(json.dumps({"skills": {"entries": {"gitlab-agent": agent}}}))
                with patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config)}):
                    self.assertEqual(reviewer.ignored_reviewers(), {"xrow", "gitlabduo"})

    def test_rejects_malformed_reviewer_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "openclaw.json"
            config.write_text(json.dumps({"skills": {"entries": {
                "gitlab-agent": {"config": {"reviewer": {"ignore": ["xrow", 7]}}}
            }}}))
            with patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config)}):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    reviewer.ignored_reviewers()

    def test_apply_preserves_existing_reviewer(self):
        result, command = self.run_selection(
            linked_items=[linked(2, "andyxrow")]
        )
        self.assertTrue(result["applied"])
        body = json.loads(command.call_args.kwargs["input"])
        self.assertEqual(body["reviewer_ids"], [2, 77])

    def test_apply_fails_if_merge_request_changed(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(
                linked_items=[linked(2, "andyxrow")], changed=True
            )


    def test_optional_approval_self_review_merges(self):
        result, command = self.run_selection(
            self_review=True, optional=True
        )
        self.assertEqual(result["rule"], "optional-approval-self-merge")
        self.assertEqual(result["reviewer"]["username"], "robot")
        self.assertTrue(result["merged"])
        calls = command.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(json.loads(calls[0].kwargs["input"]), {"reviewer_ids": [99]})
        self.assertTrue(any("/approve" in part for part in calls[1].args[0]))
        self.assertTrue(any("/merge" in part for part in calls[2].args[0]))

    def test_failed_self_approval_never_attempts_merge(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(
                self_review=True, optional=True, approval_fails=True
            )
        self.assertFalse(any(
            any(part.endswith("/merge") for part in call.args[0])
            for call in self.last_command.call_args_list
        ))

    def test_unavailable_self_approval_keeps_human_reviewer(self):
        result, _command = self.run_selection(
            self_review=True, optional=True, can_approve=False
        )
        self.assertFalse(result["self_merge"])
        self.assertEqual(result["reviewer"]["username"], "andyxrow")

    def test_insufficient_merge_access_keeps_human_reviewer(self):
        result, _command = self.run_selection(
            self_review=True, optional=True, can_merge=False
        )
        self.assertFalse(result["self_merge"])
        self.assertEqual(result["reviewer"]["username"], "andyxrow")

    def test_required_approval_keeps_human_reviewer(self):
        result, _command = self.run_selection(self_review=True, optional=False)
        self.assertFalse(result["self_merge"])
        self.assertEqual(result["reviewer"]["username"], "andyxrow")

    def test_changed_approval_rule_fails_before_writing(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_selection(
                self_review=True, optional=True, approval_changed=True
            )

    def test_draft_never_self_merges(self):
        self.assertFalse(reviewer.merge_ready({**MR, "draft": True}))

    def test_incomplete_approval_data_is_not_optional(self):
        with patch.object(reviewer, "api_text", side_effect=OSError):
            self.assertFalse(reviewer.optional_approval("projects/example/mr/7"))

    def test_pagination_loops_until_a_short_page(self):
        first_page = [{"id": value} for value in range(100)]
        with patch.object(
            reviewer, "api_text", side_effect=[json.dumps(first_page), '[{"id":100}]']
        ) as api_text:
            records = reviewer.api_pages("projects/example/members", "members")
        self.assertEqual(len(records), 101)
        self.assertIn("page=1", api_text.call_args_list[0].args[0])
        self.assertIn("page=2", api_text.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
