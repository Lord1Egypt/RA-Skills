#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for path in (SCRIPT_DIR, SKILL_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from api_task_runner import TaskRunner
from api_campaign_runner import CampaignRunner
from campaign_state_store import CampaignStateStore
from orchestrator import UpperLayerOrchestrator
from reply_processor import ReplyProcessor
import common
import run_campaign_cycle as cycle_entry


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Unsupported type: {type(value)!r}")


@contextmanager
def temp_state_dir(prefix: str):
    old_env = os.environ.get("WOTOHUB_STATE_DIR")
    old_state_dir = common._STATE_DIR
    old_settings = common._SETTINGS_PATH
    old_logs = common._LOGS_DIR
    with tempfile.TemporaryDirectory(prefix=prefix) as tmp:
        tmp_path = Path(tmp)
        os.environ["WOTOHUB_STATE_DIR"] = str(tmp_path)
        common._STATE_DIR = tmp_path
        common._SETTINGS_PATH = tmp_path / "settings.json"
        common._LOGS_DIR = tmp_path / "logs"
        try:
            yield tmp_path
        finally:
            common._STATE_DIR = old_state_dir
            common._SETTINGS_PATH = old_settings
            common._LOGS_DIR = old_logs
            if old_env is None:
                os.environ.pop("WOTOHUB_STATE_DIR", None)
            else:
                os.environ["WOTOHUB_STATE_DIR"] = old_env


def _reply_preview_fixtures() -> list[dict[str, Any]]:
    return [
        {
            "replyId": "reply-low-risk-1",
            "chatId": "chat-low-risk-1",
            "bloggerId": "creator-low-1",
            "nickname": "Alice",
            "subject": "Re: Collaboration",
            "plainTextBody": "Thanks Alice, happy to share next steps.",
            "analysisMode": "model-first",
            "classification": {
                "classification": "asks_for_next_steps",
                "intent": "asks_for_details",
                "requiresHuman": False,
            },
            "latestMail": {
                "chatId": "chat-low-risk-1",
                "bloggerId": "creator-low-1",
                "bloggerName": "Alice",
                "subject": "Re: Collaboration",
                "cleanContent": "Sounds good, please share details.",
            },
        },
        {
            "replyId": "reply-high-risk-1",
            "chatId": "chat-high-risk-1",
            "bloggerId": "creator-high-1",
            "nickname": "Bob",
            "subject": "Re: Price discussion",
            "plainTextBody": "We can offer a paid collaboration.",
            "analysisMode": "model-first",
            "classification": {
                "classification": "negotiation",
                "intent": "asks_for_price",
                "requiresHuman": True,
                "riskFlags": ["pricing"],
            },
            "latestMail": {
                "chatId": "chat-high-risk-1",
                "bloggerId": "creator-high-1",
                "bloggerName": "Bob",
                "subject": "Re: Price discussion",
                "cleanContent": "What's your budget for this collab?",
            },
        },
        {
            "replyId": "reply-invalid-1",
            "chatId": "chat-invalid-1",
            "bloggerId": "creator-invalid-1",
            "nickname": "Cara",
            "analysisMode": "model-first",
            "plainTextBody": "Missing subject should be filtered out.",
        },
    ]


def validate_reply_auto_send() -> dict[str, Any]:
    previews = _reply_preview_fixtures()
    commands = ReplyProcessor.build_commands(previews, dry_run=False)

    with temp_state_dir("wotohub-validate-reply-") as state_dir:
        def fake_subprocess_run(cmd: list[str], capture_output: bool = True, text: bool = True):
            del capture_output, text
            payload = {"code": 0, "success": True, "cmd": cmd}
            return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(payload), stderr="")

        with patch("send_reply_previews.subprocess.run", side_effect=fake_subprocess_run):
            results = ReplyProcessor.run_commands(commands, campaign_id="validation-reply")

        store = CampaignStateStore("validation-reply")
        statuses = [item.get("status") for item in results]
        blocked = [item for item in results if item.get("status") == "blocked"]
        success = [item for item in results if item.get("status") == "success"]
        action_map = store.data.get("replyActions") or {}

        ok = (
            len(success) == 1
            and len(blocked) == 1
            and "reply-invalid-1" not in {item.get("replyId") for item in results}
            and action_map.get("reply-low-risk-1", {}).get("status") == "sent"
            and action_map.get("reply-high-risk-1", {}).get("status") == "blocked"
        )

        return {
            "check": "reply_auto_send",
            "ok": ok,
            "summary": {
                "commandCount": len(commands),
                "resultCount": len(results),
                "statuses": statuses,
                "sent": len(success),
                "blocked": len(blocked),
                "filteredInvalid": True,
            },
            "stateDir": state_dir,
            "statePath": store.path,
            "results": results,
            "replyActionsState": action_map,
        }


def validate_monitor_replies() -> dict[str, Any]:
    runner = TaskRunner()
    blocked_missing_campaign = runner.run("monitor_replies", {"replyModelAnalysis": {"items": []}}, config={})
    blocked_missing_analysis = runner.run("monitor_replies", {"campaignId": "cmp-1"}, config={"token": "token"})

    monitor_payload = {
        "campaign_id": "cmp-1",
        "new_replies_count": 2,
        "replies": [
            {
                "emailId": "reply-1",
                "chatId": "chat-1",
                "bloggerId": "creator-1",
                "bloggerName": "Creator One",
                "subject": "Re: Collab",
                "content": "Interested",
                "createTime": "2026-04-08T12:00:00+00:00",
            },
            {
                "emailId": "reply-2",
                "chatId": "chat-2",
                "bloggerId": "creator-2",
                "bloggerName": "Creator Two",
                "subject": "Re: Details",
                "content": "Can you share next steps?",
                "createTime": "2026-04-08T12:30:00+00:00",
            },
        ],
    }
    valid_analysis = {
        "items": [
            {
                "replyId": "reply-1",
                "chatId": "chat-1",
                "bloggerId": "creator-1",
                "conversationStage": "reply_ready",
                "replyBody": "Thanks, sharing details soon.",
            }
        ]
    }

    with temp_state_dir("wotohub-validate-monitor-") as state_dir:
        store = CampaignStateStore("cmp-1")
        store.record_contacted("creator-1", {"nickname": "Creator One"})
        store.record_contacted("creator-2", {"nickname": "Creator Two"})

        def run_valid_case() -> dict[str, Any]:
            with patch("incremental_monitor.monitor_campaign_replies", return_value=monitor_payload):
                return runner.run(
                    "monitor_replies",
                    {
                        "campaignId": "cmp-1",
                        "replyModelAnalysis": valid_analysis,
                    },
                    config={"token": "token"},
                )

        success_case = run_valid_case()
        ok = (
            blocked_missing_campaign.get("status") == "needs_user_input"
            and "campaignId" in (blocked_missing_campaign.get("missingFields") or [])
            and blocked_missing_analysis.get("status") == "needs_user_input"
            and "replyModelAnalysis" in (blocked_missing_analysis.get("missingFields") or [])
            and success_case.get("count") == 2
            and success_case.get("campaignId") == "cmp-1"
            and len(success_case.get("replies") or []) == 2
        )
        return {
            "check": "monitor_replies",
            "ok": ok,
            "stateDir": state_dir,
            "cases": {
                "missingCampaignId": blocked_missing_campaign,
                "missingReplyModelAnalysis": blocked_missing_analysis,
                "success": success_case,
            },
        }


class _FakeCampaignRunner:
    result: dict[str, Any] = {}

    def run_cycle(self, campaign_id: str, brief: dict[str, Any], options: dict[str, Any]) -> dict[str, Any]:
        return dict(self.result)

    def build_host_model_bridge_payload(self, request: dict[str, Any], skill_root: Path) -> dict[str, Any]:
        return {"request": request, "skillRoot": str(skill_root)}


def _run_cycle_case(label: str, result_payload: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"wotohub-cycle-{label}-") as tmp:
        tmp_path = Path(tmp)
        brief_path = tmp_path / "brief.json"
        brief_path.write_text(json.dumps({"input": "validation brief"}, ensure_ascii=False, indent=2), encoding="utf-8")
        output_path = tmp_path / "output.json"

        original_argv = sys.argv[:]
        _FakeCampaignRunner.result = result_payload
        try:
            sys.argv = [
                "run_campaign_cycle.py",
                "--campaign-id", f"validation-{label}",
                "--brief", str(brief_path),
                "--output", str(output_path),
            ]
            with patch.object(cycle_entry, "CampaignRunner", _FakeCampaignRunner), patch("sys.stdout", new=io.StringIO()):
                exit_code = cycle_entry.main()
        finally:
            sys.argv = original_argv

        output = json.loads(output_path.read_text(encoding="utf-8"))
        return {
            "label": label,
            "exitCode": exit_code,
            "output": output,
            "outputPath": output_path,
        }


def validate_cycle_exit_codes() -> dict[str, Any]:
    success_case = _run_cycle_case(
        "success",
        {
            "status": "completed",
            "send": {"status": "prepared"},
            "replyActions": {"execution": {"status": "prepared"}},
        },
    )
    blocked_case = _run_cycle_case(
        "blocked",
        {
            "status": "waiting_for_host_analysis",
            "hostAnalysisRequest": {"mode": "host_analysis_request"},
        },
    )
    failed_case = _run_cycle_case(
        "failed",
        {
            "status": "failed",
            "error": {"message": "boom"},
        },
    )
    ok = (
        success_case.get("exitCode") == 0
        and blocked_case.get("exitCode") == 2
        and failed_case.get("exitCode") == 1
    )
    return {
        "check": "cycle_exit_codes",
        "ok": ok,
        "cases": {
            "success": success_case,
            "blocked": blocked_case,
            "failed": failed_case,
        },
    }


def validate_campaign_host_analysis_resolution() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="wotohub-campaign-host-analysis-") as tmp:
        tmp_path = Path(tmp)
        executor_path = tmp_path / "campaign_host_analysis_executor.py"
        executor_path.write_text(
            """
import json
import sys
from pathlib import Path

args = sys.argv[1:]
input_path = Path(args[args.index('--input') + 1])
output_path = Path(args[args.index('--output') + 1])
request = json.loads(input_path.read_text(encoding='utf-8'))
payload = {
    'host_analysis': {
        'product': {
            'productName': 'BlendGo Portable Blender',
            'brand': 'BlendGo',
            'productType': 'kitchen appliance',
            'coreBenefits': ['portable smoothies'],
        },
        'marketing': {
            'platformPreference': ['tiktok'],
            'creatorTypes': ['lifestyle'],
        },
        'constraints': {
            'regions': ['us'],
            'languages': ['en'],
            'minFansNum': 10000,
            'maxFansNum': 200000,
            'hasEmail': True,
        },
    },
    'productSummary': {
        'productName': 'BlendGo Portable Blender',
        'brand': 'BlendGo',
    },
}
output_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".strip(),
            encoding="utf-8",
        )
        executor = {
            "args": ["python3", str(executor_path), "--input", "{input}", "--output", "{output}"],
            "timeoutSeconds": 30,
        }
        runner = CampaignRunner()
        captured: dict[str, Any] = {}

        def _fake_run_engine_once(_self, _run_engine_from_brief, *, campaign_id: str, brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
            captured["campaignId"] = campaign_id
            captured["brief"] = brief
            return {
                "cycle": 1,
                "progress": {"progressPercent": 10},
                "search": {"success": True},
                "send": {"status": "prepared"},
                "replyActions": {"execution": {"status": "prepared"}},
            }

        base_brief = {
            "input": "帮我每小时搜美国 TikTok 便携榨汁杯达人并推进 sample outreach",
            "search": {"platform": "tiktok", "region": ["us"], "language": ["en"]},
            "outreach": {"cooperationType": "sample", "senderName": "Boss"},
            "draftPolicy": {"mode": "host_model_per_cycle"},
        }

        with patch.object(CampaignRunner, "_run_engine_once", new=_fake_run_engine_once):
            resolved_case = runner.run_cycle(
                "cmp-host-analysis",
                dict(base_brief),
                {"mode": "scheduled_cycle", "hostAnalysisExecutor": executor},
            )

        runtime = resolved_case.get("runtimeOrchestration") or {}
        host_runtime = runtime.get("hostAnalysis") or {}
        resolved_brief = captured.get("brief") or {}

        waiting_case = runner.run_cycle(
            "cmp-host-analysis-wait",
            dict(base_brief),
            {"mode": "scheduled_cycle"},
        )

        ok = (
            resolved_case.get("status") == "success"
            and host_runtime.get("status") == "resolved_from_executor"
            and host_runtime.get("completed") is True
            and isinstance(resolved_brief.get("model_analysis"), dict)
            and (resolved_brief.get("model_analysis") or {}).get("product", {}).get("brand") == "BlendGo"
            and waiting_case.get("status") == "waiting_for_host_analysis"
            and bool(waiting_case.get("hostAnalysisRequest"))
            and ((waiting_case.get("runtimeOrchestration") or {}).get("hostAnalysis") or {}).get("status") == "waiting_for_external_host_analysis"
        )

        return {
            "check": "campaign_host_analysis_resolution",
            "ok": ok,
            "cases": {
                "resolved": {
                    "status": resolved_case.get("status"),
                    "runtimeOrchestration": runtime,
                    "resolvedBriefModelAnalysis": resolved_brief.get("model_analysis"),
                },
                "waiting": {
                    "status": waiting_case.get("status"),
                    "runtimeOrchestration": waiting_case.get("runtimeOrchestration"),
                    "hostAnalysisRequest": waiting_case.get("hostAnalysisRequest"),
                },
            },
        }


def validate_upper_layer_host_resolution() -> dict[str, Any]:
    orchestrator = UpperLayerOrchestrator(token=None)
    with tempfile.TemporaryDirectory(prefix="wotohub-host-resolution-") as tmp:
        tmp_path = Path(tmp)
        executor_path = tmp_path / "host_bridge_executor.py"
        executor_path.write_text(
            """
import json
import sys
from pathlib import Path

args = sys.argv[1:]
input_path = Path(args[args.index('--input') + 1])
output_path = Path(args[args.index('--output') + 1])
request = json.loads(input_path.read_text(encoding='utf-8'))
mode = request.get('mode')
if mode == 'host_analysis_request':
    payload = {
        'hostAnalysis': {
            'product': {
                'productName': 'Vitamin C Serum',
                'brand': 'GlowLab',
                'productType': 'beauty',
                'productSubtype': 'serum',
                'features': ['brightening'],
                'coreBenefits': ['glow boosting'],
            },
            'marketing': {
                'platformPreference': ['tiktok'],
                'creatorTypes': ['beauty'],
            },
            'constraints': {
                'regions': ['us'],
                'languages': ['en'],
                'minFansNum': 10000,
            },
        },
        'productSummary': {
            'productName': 'Vitamin C Serum',
            'brand': 'GlowLab',
        },
    }
elif mode == 'host_reply_analysis_request':
    payload = {
        'replyModelAnalysis': {
            'items': [
                {
                    'replyId': 'reply-1',
                    'chatId': 'chat-1',
                    'bloggerId': 'creator-1',
                    'conversationStage': 'reply_ready',
                    'replyBody': 'Thanks, sending details next.',
                }
            ]
        }
    }
elif mode == 'host_draft_request':
    payload = {
        'hostDrafts': [
            {
                'bloggerId': 'creator-1',
                'subject': 'BlendGo x creator-1',
                'plainTextBody': 'Hi creator-1',
                'htmlBody': '<p>Hi creator-1</p>',
            }
        ]
    }
else:
    payload = {}
output_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".strip(),
            encoding="utf-8",
        )
        executor = {
            "args": ["python3", str(executor_path), "--input", "{input}", "--output", "{output}"],
            "timeoutSeconds": 30,
        }

        search_case = orchestrator.run_from_user_input(
            "帮我搜索美国 TikTok 便携榨汁杯达人",
            explicit_task="search",
            config={"hostAnalysisExecutor": executor},
        )
        monitor_case = orchestrator.run_from_user_input(
            "检查这个 campaign 的新回复",
            explicit_task="monitor_replies",
            request_passthrough={"campaignId": "cmp-1"},
            config={"hostReplyBridgeExecutor": executor},
        )
        generate_case = orchestrator.run_from_user_input(
            "帮我给美国 TikTok 达人写 sample 合作开发信",
            explicit_task="generate_email",
            config={"hostAnalysisExecutor": executor, "hostDraftExecutor": executor},
        )

        search_resolution = ((search_case.get("observations") or {}).get("hostResolution") or {}).get("hostAnalysis") or {}
        monitor_resolution = ((monitor_case.get("observations") or {}).get("hostResolution") or {}).get("replyModelAnalysis") or {}
        generate_resolution = (generate_case.get("observations") or {}).get("hostResolution") or {}
        draft_resolution = generate_resolution.get("hostDrafts") or {}
        generate_analysis_resolution = generate_resolution.get("hostAnalysis") or {}

        ok = (
            search_case.get("delegatedTask") == "search"
            and not ((search_case.get("route") or {}).get("missingFields") or [])
            and search_resolution.get("status") == "resolved_from_executor"
            and search_resolution.get("fulfilled") is True
            and monitor_case.get("delegatedTask") == "monitor_replies"
            and not ((monitor_case.get("route") or {}).get("missingFields") or [])
            and monitor_resolution.get("status") == "resolved_from_executor"
            and monitor_resolution.get("fulfilled") is True
            and generate_case.get("delegatedTask") == "generate_email"
            and not ((generate_case.get("route") or {}).get("missingFields") or [])
            and generate_analysis_resolution.get("status") == "resolved_from_executor"
            and generate_analysis_resolution.get("fulfilled") is True
            and draft_resolution.get("status") == "resolved_from_executor"
            and draft_resolution.get("fulfilled") is True
        )

        return {
            "check": "upper_layer_host_resolution",
            "ok": ok,
            "cases": {
                "search": {
                    "delegatedTask": search_case.get("delegatedTask"),
                    "missingFields": (search_case.get("route") or {}).get("missingFields"),
                    "hostResolution": search_resolution,
                },
                "monitor_replies": {
                    "delegatedTask": monitor_case.get("delegatedTask"),
                    "missingFields": (monitor_case.get("route") or {}).get("missingFields"),
                    "hostResolution": monitor_resolution,
                },
                "generate_email": {
                    "delegatedTask": generate_case.get("delegatedTask"),
                    "missingFields": (generate_case.get("route") or {}).get("missingFields"),
                    "hostResolution": generate_resolution,
                },
            },
        }


CHECKS: dict[str, Callable[[], dict[str, Any]]] = {
    "reply_auto_send": validate_reply_auto_send,
    "monitor_replies": validate_monitor_replies,
    "cycle_exit_codes": validate_cycle_exit_codes,
    "campaign_host_analysis_resolution": validate_campaign_host_analysis_resolution,
    "upper_layer_host_resolution": validate_upper_layer_host_resolution,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Release validation for WotoHub automation")
    parser.add_argument(
        "--check",
        choices=["all", *CHECKS.keys()],
        default="all",
        help="Validation check to run",
    )
    args = parser.parse_args()

    selected = CHECKS.items() if args.check == "all" else [(args.check, CHECKS[args.check])]
    reports = []
    ok = True
    for _, func in selected:
        report = func()
        reports.append(report)
        ok = ok and bool(report.get("ok"))

    payload = {
        "ok": ok,
        "checks": reports,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
