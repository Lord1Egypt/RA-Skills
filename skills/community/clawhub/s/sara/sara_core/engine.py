from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    before: str
    after: str
    reason: str
    severity: str = "high"


class SaraAuditor:
    """
    Minimal deterministic auditor for OpenClaw multi-skill workflows.

    v0.1 scope:
    - backup -> delete
    - check -> operate
    - permission -> read
    - preview -> publish
    """

    def __init__(self) -> None:
        # Normalize many tool/skill verbs into a small set of logical action classes.
        self.aliases = {
            # -------------------------
            # backup / export / snapshot
            # -------------------------
            "backup": "backup",
            "create_backup": "backup",
            "export_backup": "backup",
            "snapshot": "backup",
            "archive": "backup",
            "save_copy": "backup",
            "mirror": "backup",
            "mirror_repo": "backup",
            "backup_repo": "backup",
            "github_backup_repo": "backup",
            "clone_repo": "backup",
            "bundle_repo": "backup",
            "dump_db": "backup",
            "export_db": "backup",
            "pg_dump": "backup",
            "mysqldump": "backup",
            "sqlite_backup": "backup",
            "download_export": "backup",

            # -------------------------
            # delete / remove / destructive mutation
            # -------------------------
            "delete": "delete",
            "remove": "delete",
            "clear": "delete",
            "wipe": "delete",
            "erase": "delete",
            "purge": "delete",
            "trash": "delete",
            "trash_file": "delete",
            "delete_file": "delete",
            "delete_folder": "delete",
            "delete_repo": "delete",
            "github_delete_repo": "delete",
            "drop_db": "delete",
            "drop_database": "delete",
            "drop_table": "delete",
            "truncate_table": "delete",
            "reset_hard": "delete",
            "force_remove": "delete",

            # -------------------------
            # check / validate / inspect / review
            # -------------------------
            "check": "check",
            "inspect": "check",
            "verify": "check",
            "validate": "check",
            "review": "check",
            "review_draft": "check",
            "review_pr": "check",
            "preview": "check",   # generic preview/check intent
            "check_calendar": "check",
            "check_availability": "check",
            "check_conflicts": "check",
            "check_status": "check",
            "healthcheck": "check",
            "dry_run": "check",
            "lint": "check",
            "test_run": "check",
            "run_tests": "check",
            "status_repo": "check",
            "git_status": "check",
            "diff": "check",
            "git_diff": "check",
            "show_plan": "check",

            # -------------------------
            # operate / booking / sending / applying
            # -------------------------
            "operate": "operate",
            "apply_changes": "operate",
            "execute": "operate",
            "run": "operate",
            "book_flight": "operate",
            "book_hotel": "operate",
            "schedule_meeting": "operate",
            "modify_calendar": "operate",
            "send_email": "operate",
            "send_message": "operate",
            "reply_email": "operate",
            "submit_payment": "operate",
            "create_invoice": "operate",
            "merge_pr": "operate",
            "merge_branch": "operate",
            "push_branch": "operate",
            "commit_changes": "operate",
            "update_record": "operate",
            "insert_row": "operate",
            "write_db": "operate",

            # -------------------------
            # permission / auth / access grant
            # -------------------------
            "permission": "permission",
            "get_permission": "permission",
            "request_permission": "permission",
            "request_access": "permission",
            "authorize": "permission",
            "auth": "permission",
            "login": "permission",
            "sign_in": "permission",
            "grant_access": "permission",
            "unlock": "permission",
            "approve_access": "permission",

            # -------------------------
            # read / fetch / download private data
            # -------------------------
            "read": "read",
            "read_data": "read",
            "read_private_data": "read",
            "fetch_private": "read",
            "fetch_data": "read",
            "query_data": "read",
            "download": "read",
            "download_file": "read",
            "read_csv": "read",
            "read_sheet": "read",
            "export_report": "read",
            "select_rows": "read",

            # -------------------------
            # preview / draft / summarize before publish
            # -------------------------
            "preview_output": "preview",
            "draft": "preview",
            "compose_draft": "preview",
            "generate_draft": "preview",
            "summarize": "preview",
            "generate_summary": "preview",
            "preview_post": "preview",
            "render_preview": "preview",
            "preview_newsletter": "preview",

            # -------------------------
            # publish / post / send to external audience
            # -------------------------
            "publish": "publish",
            "publish_post": "publish",
            "publish_blog": "publish",
            "post": "publish",
            "post_to_main": "publish",
            "tweet": "publish",
            "post_tweet": "publish",
            "post_linkedin": "publish",
            "post_discord": "publish",
            "post_slack": "publish",
            "send_newsletter": "publish",
            "send_campaign": "publish",
            "push_live": "publish",
            "deploy_live": "publish",
        }

        self.rules: list[Rule] = [
            Rule(
                before="backup",
                after="delete",
                reason="Backups should happen before destructive actions.",
                severity="critical",
            ),
            Rule(
                before="check",
                after="operate",
                reason="Checks should happen before irreversible or high-impact actions.",
                severity="high",
            ),
            Rule(
                before="permission",
                after="read",
                reason="Permission or access grant should happen before reading sensitive data.",
                severity="critical",
            ),
            Rule(
                before="preview",
                after="publish",
                reason="Preview or draft review should happen before publishing to an external audience.",
                severity="high",
            ),
        ]

        self.priority = {
            "backup": 10,
            "permission": 15,
            "check": 20,
            "read": 40,
            "preview": 50,
            "operate": 80,
            "publish": 85,
            "delete": 90,
        }

    def normalize_tool(self, tool_name: str) -> str:
        key = (tool_name or "").strip().lower()
        return self.aliases.get(key, key)

    def normalize_sequence(self, tools_sequence: Iterable[str]) -> list[str]:
        return [self.normalize_tool(t) for t in tools_sequence if t]

    def _find_violations(self, normalized_tools: list[str]) -> list[dict]:
        violations: list[dict] = []

        for rule in self.rules:
            if rule.before in normalized_tools and rule.after in normalized_tools:
                before_idx = normalized_tools.index(rule.before)
                after_idx = normalized_tools.index(rule.after)

                if before_idx > after_idx:
                    violations.append(
                        {
                            "type": "order_violation",
                            "severity": rule.severity,
                            "message": f"Run '{rule.before}' before '{rule.after}'. {rule.reason}",
                            "before": rule.before,
                            "after": rule.after,
                        }
                    )

        return violations

    def _risk_level(self, violations: list[dict]) -> str:
        if not violations:
            return "low"
        if any(v["severity"] == "critical" for v in violations):
            return "critical"
        return "high"

    def _suggested_order(self, normalized_tools: list[str]) -> list[str]:
        indexed = list(enumerate(normalized_tools))

        def sort_key(item: tuple[int, str]) -> tuple[int, int]:
            idx, tool = item
            return (self.priority.get(tool, 50), idx)

        return [tool for _, tool in sorted(indexed, key=sort_key)]

    def audit_trajectory(self, tools_sequence: Iterable[str]) -> dict:
        normalized_tools = self.normalize_sequence(tools_sequence)
        violations = self._find_violations(normalized_tools)

        return {
            "is_safe": len(violations) == 0,
            "risk_level": self._risk_level(violations),
            "warnings": [v["message"] for v in violations],
            "violations": violations,
            "normalized_tools": normalized_tools,
            "suggested_order": self._suggested_order(normalized_tools) if violations else None,
        }
