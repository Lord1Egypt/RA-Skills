from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv

from .approvals import ApprovalGate
from .cluster_live import fetch_cluster_incidents
from .config import Settings
from .digest import build_report, draft_reply_for_item
from .discord_live import fetch_discord_snapshot
from .fixtures import load_fixture_messages
from .kubewatch import (
    build_kubewatch_report,
    fetch_apify_incidents,
    load_kubewatch_fixture,
    load_kubewatch_history,
)
from .memory import build_state_store
from .models import SituationItem


def main() -> None:
    load_dotenv()
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mts",
        description="Situation Monitor: digest Discord traffic and Kubernetes incidents into ranked operational reports.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fixture = subparsers.add_parser("fixture", help="Run the offline fixture demo.")
    fixture.add_argument("--input", type=Path, required=True)
    fixture.add_argument("--save-path", type=Path)
    fixture.set_defaults(func=_run_fixture)

    discord_fetch = subparsers.add_parser(
        "discord-fetch",
        help="Fetch a one-shot live Discord snapshot from bot-visible channels.",
    )
    discord_fetch.add_argument("--hours", type=int, default=24)
    discord_fetch.add_argument("--limit-per-channel", type=int, default=75)
    discord_fetch.add_argument("--save-path", type=Path)
    discord_fetch.set_defaults(func=_run_discord_fetch)

    draft = subparsers.add_parser(
        "draft-reply",
        help="Draft a reply from the latest saved report.",
    )
    draft.add_argument(
        "--bucket",
        choices=["urgent", "direct_asks", "decisions", "fyi"],
        required=True,
    )
    draft.add_argument("--channel", required=True)
    draft.set_defaults(func=_run_draft_reply)

    kubewatch_fixture = subparsers.add_parser(
        "kubewatch-fixture",
        help="Run the KubeWatch fixture demo.",
    )
    kubewatch_fixture.add_argument("--input", type=Path, required=True)
    kubewatch_fixture.add_argument("--save-path", type=Path)
    kubewatch_fixture.set_defaults(func=_run_kubewatch_fixture)

    kubewatch_apify = subparsers.add_parser(
        "kubewatch-apify",
        help="Run KubeWatch against a live Apify actor dataset.",
    )
    kubewatch_apify.add_argument("--actor-id")
    kubewatch_apify.add_argument("--actor-input", type=Path)
    kubewatch_apify.add_argument("--save-path", type=Path)
    kubewatch_apify.set_defaults(func=_run_kubewatch_apify)

    kubewatch_history = subparsers.add_parser(
        "kubewatch-history",
        help="Show recent KubeWatch incident history from state.",
    )
    kubewatch_history.add_argument("--limit", type=int, default=5)
    kubewatch_history.set_defaults(func=_run_kubewatch_history)

    kubewatch_cluster = subparsers.add_parser(
        "kubewatch-cluster",
        help="Scan the live Kubernetes cluster via kubectl and emit a KubeWatch report.",
    )
    kubewatch_cluster.add_argument("--namespace")
    kubewatch_cluster.add_argument("--save-path", type=Path)
    kubewatch_cluster.set_defaults(func=_run_kubewatch_cluster)

    return parser


def _run_fixture(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    settings.ensure_state_dir()
    store = build_state_store(settings.redis_url, settings.state_path)
    messages = load_fixture_messages(args.input)
    report = build_report(messages, settings=settings, source=f"fixture:{args.input.name}")
    store.save_latest_report(report)
    store.save_checkpoint(report.source, report.generated_at)
    _emit_report(report.to_markdown(), args.save_path)


def _run_discord_fetch(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    settings.ensure_state_dir()
    store = build_state_store(settings.redis_url, settings.state_path)
    messages = asyncio.run(
        fetch_discord_snapshot(
            settings, hours=args.hours, limit_per_channel=args.limit_per_channel
        )
    )
    report = build_report(messages, settings=settings, source="discord:live")
    store.save_latest_report(report)
    store.save_checkpoint(report.source, report.generated_at)
    _emit_report(report.to_markdown(), args.save_path)


def _run_draft_reply(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    store = build_state_store(settings.redis_url, settings.state_path)
    report = store.load_latest_report()
    if report is None:
        raise SystemExit("No saved report found. Run fixture or discord-fetch first.")

    decision = ApprovalGate(settings).check("draft_reply")
    if not decision.allowed:
        raise SystemExit(decision.reason)

    item = _find_item(report, args.bucket, args.channel)
    if item is None:
        raise SystemExit(
            f"No item found for bucket={args.bucket} channel={args.channel}."
        )
    print(draft_reply_for_item(item, settings))


def _run_kubewatch_fixture(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    settings.ensure_state_dir()
    incidents = load_kubewatch_fixture(args.input)
    report = build_kubewatch_report(
        incidents, settings=settings, source=f"kubewatch-fixture:{args.input.name}"
    )
    _emit_report(report.to_markdown(), args.save_path)


def _run_kubewatch_apify(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    settings.ensure_state_dir()
    incidents = fetch_apify_incidents(
        settings,
        actor_id=args.actor_id,
        actor_input_path=args.actor_input,
    )
    report = build_kubewatch_report(
        incidents, settings=settings, source="kubewatch-apify"
    )
    _emit_report(report.to_markdown(), args.save_path)


def _run_kubewatch_history(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    history = load_kubewatch_history(settings, limit=args.limit)
    if not history:
        print("No KubeWatch history found.")
        return
    for incident in history:
        print(
            f"- {incident.started_at.isoformat()} | {incident.service} | "
            f"{incident.title} | {incident.source}"
        )


def _run_kubewatch_cluster(args: argparse.Namespace) -> None:
    settings = Settings.from_env()
    settings.ensure_state_dir()
    try:
        incidents = fetch_cluster_incidents(settings, namespace=args.namespace)
    except ValueError as exc:
        raise SystemExit(str(exc))
    report = build_kubewatch_report(
        incidents,
        settings=settings,
        source=f"kubewatch-cluster:{args.namespace or settings.kube_namespace}",
    )
    _emit_report(report.to_markdown(), args.save_path)


def _find_item(report, bucket: str, channel: str) -> SituationItem | None:
    items = getattr(report, bucket)
    for item in items:
        if item.channel == channel:
            return item
    return None


def _emit_report(markdown: str, save_path: Path | None) -> None:
    print(markdown)
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(markdown)
