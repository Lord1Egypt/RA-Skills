from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess
from typing import Any

MANAGED_CRON_NAMES = [
    "sherpamind:hot-open-sync",
    "sherpamind:warm-closed-sync",
    "sherpamind:cold-closed-audit",
    "sherpamind:priority-enrichment",
    "sherpamind:public-snapshot",
    "sherpamind:doctor",
]


@dataclass(frozen=True)
class CronCleanupResult:
    status: str
    removed: list[dict[str, Any]]
    found: list[dict[str, Any]]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=True)


def list_cron_jobs() -> dict[str, Any]:
    result = _run(["openclaw", "cron", "list", "--json"])
    return json.loads(result.stdout)


def managed_jobs() -> list[dict[str, Any]]:
    jobs = list_cron_jobs().get("jobs", [])
    return [job for job in jobs if job.get("name") in MANAGED_CRON_NAMES]


def doctor_automation() -> dict[str, Any]:
    jobs = managed_jobs()
    counts: dict[str, int] = {}
    for job in jobs:
        counts[job["name"]] = counts.get(job["name"], 0) + 1
    duplicates = {name: count for name, count in counts.items() if count > 1}
    return {
        "managed_cron_names": MANAGED_CRON_NAMES,
        "found_names": sorted(counts.keys()),
        "duplicates": duplicates,
        "job_count": len(jobs),
        "status": "present" if jobs else "absent",
        "note": "SherpaMind no longer uses OpenClaw cron for normal background runtime; any managed cron jobs should usually be removed.",
    }


def remove_managed_cron_jobs() -> CronCleanupResult:
    jobs = managed_jobs()
    removed = []
    for job in jobs:
        _run(["openclaw", "cron", "remove", job["id"], "--json"])
        removed.append({"id": job["id"], "name": job["name"]})
    return CronCleanupResult(status="ok", removed=removed, found=jobs)
