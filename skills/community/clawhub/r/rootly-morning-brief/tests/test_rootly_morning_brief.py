import datetime as dt
import importlib.util
import sys
from pathlib import Path
import unittest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "rootly_morning_brief.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("rootly_morning_brief", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


brief = _load_module()


class SelectActiveAndRecentIncidentsTests(unittest.TestCase):
    def test_recent_resolved_without_resolved_at_uses_created_at_proxy(self):
        now = dt.datetime(2026, 3, 15, 12, 0, tzinfo=dt.timezone.utc)
        items = [
            {
                "id": "inc_1",
                "attributes": {
                    "title": "Database failover completed",
                    "status": "resolved",
                    "created_at": "2026-03-15T10:30:00+00:00",
                    "summary": "Resolved cleanly but without a resolved_at timestamp",
                    "severity": {"data": {"attributes": {"name": "sev2"}}},
                    "private": False,
                    "url": "https://root.ly/inc_1",
                },
            }
        ]

        active, resolved = brief.select_active_and_recent_incidents(items, now)

        self.assertEqual(active, [])
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0].title, "Database failover completed")
        self.assertIsNone(resolved[0].resolved_at)
        message = brief.format_digest(
            active_incidents=[],
            recent_resolved_incidents=resolved,
            current_oncalls=[],
            overdue_action_items=[],
            include_private=False,
            now_local=now.astimezone(brief.ZoneInfo("America/Toronto")),
            timezone=brief.ZoneInfo("America/Toronto"),
            max_items=5,
        )
        self.assertIn(
            "• <https://root.ly/inc_1|Database failover completed> — resolved recently",
            message,
        )


class SelectCurrentOncallsTests(unittest.TestCase):
    def test_reads_user_and_level_from_real_oncall_shape(self):
        now = dt.datetime(2026, 3, 15, 18, 0, tzinfo=dt.timezone.utc)
        items = [
            {
                "id": "oncall_1",
                "attributes": {
                    "escalation_policy_name": "escalation policy",
                    "escalation_level": 2,
                    "schedule_name": "On call schedule",
                    "user_id": 233906,
                    "starts_at": "2026-03-15T10:17:06.000-07:00",
                    "ends_at": "2026-04-16T00:00:00.000-07:00",
                },
                "relationships": {
                    "user": {"data": {"id": "233906", "type": "users"}},
                    "schedule": {
                        "data": {"id": "sched_1", "type": "schedules"}
                    },
                    "escalation_policy": {
                        "data": {"id": "policy_1", "type": "escalation_policies"}
                    },
                },
            }
        ]
        included = [
            {
                "id": "233906",
                "type": "users",
                "attributes": {"full_name": "Nicole Bu"},
            },
            {
                "id": "sched_1",
                "type": "schedules",
                "attributes": {"name": "On call schedule"},
            },
            {
                "id": "policy_1",
                "type": "escalation_policies",
                "attributes": {"name": "escalation policy"},
            },
        ]

        current = brief.select_current_oncalls(items, included, now)

        self.assertEqual(len(current), 1)
        self.assertEqual(current[0].name, "Nicole Bu")
        self.assertEqual(current[0].schedule, "On call schedule")
        self.assertEqual(current[0].policy_name, "escalation policy")
        self.assertEqual(current[0].policy_level, 2)
        self.assertEqual(
            brief._line_for_oncall(current[0]),
            "• Nicole Bu — L2 secondary",
        )


class SelectOverdueActionItemsTests(unittest.TestCase):
    def test_selects_only_open_past_due_items(self):
        now = dt.datetime(2026, 3, 15, 16, 0, tzinfo=dt.timezone.utc)
        items = [
            {
                "id": "ai_1",
                "attributes": {
                    "summary": "Rotate CI deploy tokens and validate revocation",
                    "status": "in_progress",
                    "priority": "high",
                    "due_date": "2026-03-15T10:00:00+00:00",
                    "jira_issue_key": "SEC-742",
                    "incident_title": "Global sign-in failures after OIDC key rotation",
                    "assigned_to": {
                        "first_name": "Nicole",
                        "last_name": "Bu",
                        "email": "nicole@example.com",
                    },
                    "short_url": "https://root.ly/ai_1",
                },
            },
            {
                "id": "ai_2",
                "attributes": {
                    "summary": "Closed follow-up should be filtered out",
                    "status": "done",
                    "priority": "high",
                    "due_date": "2026-03-15T08:00:00+00:00",
                    "incident_title": "Global sign-in failures after OIDC key rotation",
                    "assigned_to": {"first_name": "Jordan", "last_name": "Patel"},
                    "short_url": "https://root.ly/ai_2",
                },
            },
            {
                "id": "ai_3",
                "attributes": {
                    "summary": "Future due follow-up should not be overdue",
                    "status": "in_progress",
                    "priority": "medium",
                    "due_date": "2026-03-16T08:00:00+00:00",
                    "incident_title": "Global sign-in failures after OIDC key rotation",
                    "assigned_to": {"first_name": "Alex", "last_name": "Kim"},
                    "short_url": "https://root.ly/ai_3",
                },
            },
        ]

        overdue = brief.select_overdue_action_items(items, now)

        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].id, "ai_1")
        self.assertEqual(overdue[0].assignee, "Nicole Bu")
        self.assertEqual(overdue[0].ticket_key, "SEC-742")
        rendered = brief._line_for_action_item(
            overdue[0],
            brief.ZoneInfo("America/Toronto"),
        )
        self.assertIn("⚠️", rendered)
        self.assertIn("[P1]", rendered)
        self.assertIn("SEC-742", rendered)


class FormatDigestOrderingTests(unittest.TestCase):
    def test_active_incidents_prioritize_severity_over_recency(self):
        tz = brief.ZoneInfo("America/Toronto")
        now = dt.datetime(2026, 3, 15, 12, 0, tzinfo=dt.timezone.utc)
        sev2_newer = brief.Incident(
            id="inc_sev2",
            title="SEV2 newer incident",
            status="started",
            severity="SEV2",
            url="https://root.ly/inc_sev2",
            created_at=dt.datetime(2026, 3, 15, 11, 58, tzinfo=dt.timezone.utc),
            resolved_at=None,
        )
        sev0_older = brief.Incident(
            id="inc_sev0",
            title="SEV0 older incident",
            status="started",
            severity="SEV0",
            url="https://root.ly/inc_sev0",
            created_at=dt.datetime(2026, 3, 15, 11, 30, tzinfo=dt.timezone.utc),
            resolved_at=None,
        )

        message = brief.format_digest(
            active_incidents=[sev2_newer, sev0_older],
            recent_resolved_incidents=[],
            current_oncalls=[],
            overdue_action_items=[],
            include_private=False,
            now_local=now.astimezone(tz),
            timezone=tz,
            max_items=5,
        )

        self.assertIn("At a glance: 2 active (1 SEV0/SEV1)", message)
        self.assertLess(
            message.find("SEV0 older incident"),
            message.find("SEV2 newer incident"),
        )


if __name__ == "__main__":
    unittest.main()
