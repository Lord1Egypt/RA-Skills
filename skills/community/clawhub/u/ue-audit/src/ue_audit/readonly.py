"""Read-only bridge allowlist and audit-side-effect evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .bridge import BridgeClient, BridgeError
from .manifest import Manifest, diff_is_empty, diff_manifests


READ_ONLY_COMMANDS = frozenset(
    {
        "health",
        "list_assets",
        "read_blueprint",
        "read_variables",
        "read_cdo",
        "read_nodes",
        "read_connections",
        "search_blueprint_nodes",
        "get_pin_default_value",
        "get_node_by_guid",
        "pie_state",
        "find_actors",
        "get_actor_properties",
        "logs_read",
        "material_read",
        "widget_read_tree",
        "datatable_read",
        "class_probe",
        "animbp_probe",
        "animbp_read",
        "debug_reflect",
        "session_lock_status",
        "receipt_list",
        "task_list",
        "task_assets",
        "agent_undo_status",
    }
)


STATEFUL_COMMANDS = frozenset({"pie_start", "pie_stop"})


class ReadOnlyViolation(RuntimeError):
    pass


@dataclass
class ReadOnlyBridge:
    client: BridgeClient
    allowlist: frozenset[str] = READ_ONLY_COMMANDS

    def call(self, command: str, params: dict[str, Any] | None = None) -> Any:
        if command not in self.allowlist:
            raise ReadOnlyViolation(f"command is not allow-listed for read-only audit: {command}")
        return self.client.call(command, params)

    def call_stateful(self, command: str, params: dict[str, Any] | None = None) -> Any:
        """Explicit opt-in for stateful runtime commands (PIE start/stop)."""
        if command not in STATEFUL_COMMANDS:
            raise ReadOnlyViolation(f"command is not an allowed stateful command: {command}")
        return self.client.call(command, params)

    def health(self) -> dict[str, Any]:
        return self.client.health()


def build_readonly_proof(
    before: Manifest,
    after: Manifest,
    write_monitor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    diff = diff_manifests(before, after)
    content_equal = not (
        diff["added_count"] or diff["removed_count"] or diff["changed_count"]
    )
    metadata_equal = diff["metadata_changed_count"] == 0
    unknown_count = diff["unknown_count"]

    monitor = write_monitor or {}
    monitor_available = bool(monitor.get("available"))
    events = monitor.get("events") or []
    event_count = int(monitor.get("event_count") or len(events))
    overflow = bool(monitor.get("overflow"))
    during_write_clean = (event_count == 0 and not overflow) if monitor_available else None
    no_observed_difference = (
        content_equal
        and metadata_equal
        and unknown_count == 0
        and during_write_clean is not False
    )

    if not content_equal:
        statement = "Project content changed during the audit; the audit was not read-only."
    elif not metadata_equal:
        statement = (
            "File hashes are unchanged, but file metadata changed during the audit. "
            "This may indicate a touch or save without content change."
        )
    elif unknown_count:
        statement = (
            "No content hash changes were observed, but one or more files could not be "
            "hashed; completeness of the read-only observation is unknown."
        )
    elif monitor_available and not during_write_clean:
        statement = (
            "The manifest is unchanged, but file-system events were observed during the "
            "audit. Inspect the event list; the audit may have touched files outside the "
            "manifest or the editor may have written while the audit ran."
        )
    elif monitor_available:
        statement = (
            "No content or metadata difference and no directory write events were observed "
            "between the start and end of this audit. This is still an observation, not "
            "absolute proof that no write occurred."
        )
    else:
        statement = (
            "No content or metadata difference was observed between the start and end "
            "of this audit. The during-write monitor was unavailable, so this is an "
            "observation, not absolute proof that no write occurred."
        )

    limitations = [
        "Manifest comparison only covers the configured roots and exclusion rules.",
        "A write followed by a restore to the same bytes and metadata would not be detected.",
        "Editor memory state, registry, and external processes are not observed.",
    ]
    if monitor_available:
        limitations.append(
            "The during-write monitor is best-effort ReadDirectoryChangesW over the "
            "configured roots, not kernel ETW/USN; events outside the roots may be missed."
        )
    else:
        limitations.append(
            "The during-write monitor was unavailable; only before/after manifests were compared."
        )

    return {
        "before_manifest_sha256": before.manifest_sha256,
        "after_manifest_sha256": after.manifest_sha256,
        "content_equal": content_equal,
        "metadata_equal": metadata_equal,
        "no_observed_difference": no_observed_difference,
        "unknown_count": unknown_count,
        "diff": diff,
        "during_write_monitor": "available" if monitor_available else "unavailable",
        "during_write_clean": during_write_clean,
        "during_write_event_count": event_count,
        "during_write_events": events[:200],
        "during_write_overflow": overflow,
        "during_write_reason": monitor.get("reason", ""),
        "during_write_limitation": monitor.get("limitation", ""),
        "statement": statement,
        "limitations": limitations,
    }


def diff_is_readonly(diff: dict[str, Any]) -> bool:
    return diff_is_empty(diff, include_metadata=True)
