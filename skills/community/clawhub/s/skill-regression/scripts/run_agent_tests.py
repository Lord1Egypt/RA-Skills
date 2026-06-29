#!/usr/bin/env python3
"""
run_agent_tests.py — Execute the AI/agent layer of tests (dual-backend).

Two backends:
  - `api`      : OpenAI-compatible LLM acts as the skill (uses SKILL.md as system prompt).
                  Stateless, parallel-safe, works anywhere.
  - `openclaw` : Real OpenClaw agent triggered via cron probe job.
                  Tests true agent + skill end-to-end; only works inside OpenClaw runtime.

Both backends use the same scoring layer (LLM-as-judge, configurable model).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_config import resolve_config, require_config_ready  # noqa: E402
from _lib_llm import score_response, simulate_skill_response  # noqa: E402


HARD_CASE_TIMEOUT_BUFFER = 30


# ─── Args ─────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--cases", required=True, help="Path to cases.json")
    p.add_argument("--output", required=True, help="Path to agent_results.json")
    p.add_argument("--threshold", type=float, default=7.0)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--space-dir", required=True)
    p.add_argument("--skip", action="store_true",
                   help="Skip all AI tests (mark as skipped)")
    p.add_argument("--cases-filter", default="",
                   help="Comma-separated case IDs to run (used by --rerun)")
    p.add_argument("--backend", default="",
                   help="openclaw | api (overrides config)")
    return p.parse_args()


# ─── OpenClaw cron-based backend ─────────────────────────────────────

PROBE_FILE_NAME = "probe.json"


def _openclaw_available() -> bool:
    try:
        subprocess.run(["openclaw", "--help"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def _ensure_probe_job(space_dir: str, agent_name: str) -> dict:
    """Create or reuse a cron probe job for this agent."""
    probe_file = Path(space_dir) / PROBE_FILE_NAME
    existing = {}
    if probe_file.exists():
        try:
            existing = json.loads(probe_file.read_text())
        except Exception:
            existing = {}

    job_id = existing.get("job_id", "")
    if job_id and existing.get("agent_name") == agent_name:
        # Verify still alive
        try:
            r = subprocess.run(
                ["openclaw", "cron", "list", "--json"],
                capture_output=True, text=True, timeout=10,
            )
            if job_id in r.stdout:
                return existing
        except Exception:
            return existing  # Don't fail if cron list errors

    # Create new namespaced job
    job_name = f"skill-regression-probe-{agent_name}-{uuid.uuid4().hex[:8]}"
    print(f"  Creating probe job: {job_name}", file=sys.stderr)
    try:
        result = subprocess.run(
            [
                "openclaw", "cron", "add",
                "--name", job_name,
                "--session", "isolated",
                "--message", "placeholder",
                "--at", "2099-01-01T00:00:00Z",
                "--keep-after-run",
                "--light-context",
                "--no-deliver",
                "--json",
            ],
            capture_output=True, text=True, timeout=20,
        )
        if result.returncode != 0:
            raise RuntimeError(f"cron add failed: {result.stderr[:300]}")
        out = result.stdout.strip()
        start = out.find("{")
        if start != -1:
            out = out[start:]
        data = json.loads(out)
        job_id = data.get("id") or data.get("jobId") or ""
        info = {"job_id": job_id, "agent_name": agent_name, "session_key": f"agent:{agent_name}:cron:{job_id}"}
        probe_file.parent.mkdir(parents=True, exist_ok=True)
        probe_file.write_text(json.dumps(info, indent=2))
        return info
    except Exception as e:
        raise RuntimeError(f"Failed to create probe job: {e}")


def _trigger_openclaw_agent(probe: dict, trigger: str, timeout: int) -> str:
    """Trigger the probe job with a custom message; return assistant reply."""
    job_id = probe["job_id"]
    # Edit message
    edit = subprocess.run(
        ["openclaw", "cron", "edit", job_id, "--message", trigger],
        capture_output=True, text=True, timeout=10,
    )
    if edit.returncode != 0:
        raise RuntimeError(f"cron edit failed: {edit.stderr[:200]}")

    # Trigger run (fire-and-forget)
    send_time = time.time()
    subprocess.Popen(
        ["openclaw", "cron", "run", job_id],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Poll sessions.json for the new session triggered by this run
    sessions_path = Path(f"~/.openclaw/agents/{probe['agent_name']}/sessions/sessions.json").expanduser()
    if not sessions_path.exists():
        raise RuntimeError(
            f"sessions.json not found: {sessions_path}\n"
            f"Make sure target agent '{probe['agent_name']}' exists in OpenClaw."
        )

    # Wait for new session_id (5s tolerance for write lag)
    session_id = None
    deadline = send_time + 60
    while time.time() < deadline:
        try:
            d = json.loads(sessions_path.read_text())
            for skey, entry in d.items():
                if not skey.startswith(f"agent:{probe['agent_name']}:cron:{job_id}"):
                    continue
                created_ts = entry.get("createdAt", 0) / 1000.0
                if created_ts >= send_time - 5:
                    session_id = entry.get("sessionId")
                    if session_id:
                        break
        except Exception:
            pass
        if session_id:
            break
        time.sleep(1)

    if not session_id:
        raise TimeoutError(f"Probe session not created within 60s (agent={probe['agent_name']})")

    # Poll jsonl for assistant reply
    jsonl = Path(f"~/.openclaw/agents/{probe['agent_name']}/sessions/{session_id}.jsonl").expanduser()
    deadline = send_time + timeout
    while time.time() < deadline:
        if jsonl.exists():
            try:
                for line in jsonl.read_text().splitlines():
                    obj = json.loads(line)
                    if obj.get("role") == "assistant" and obj.get("content"):
                        content = obj["content"]
                        if isinstance(content, list):
                            # Extract text segments
                            content = "".join(
                                p.get("text", "") for p in content if isinstance(p, dict)
                            )
                        if content:
                            return content
            except Exception:
                pass
        time.sleep(2)

    raise TimeoutError(f"No assistant reply within {timeout}s (session={session_id})")


# ─── Test execution ──────────────────────────────────────────────────

def _run_one_case(case: dict, backend: str, cfg: dict, probe: dict, threshold: float, timeout: int, skill_md: str) -> dict:
    """Run a single case end-to-end."""
    case_id = case.get("id", "?")
    trigger = case.get("trigger", "")
    expected = case.get("expected_agent_response", "")

    if case.get("skip_agent"):
        return {"id": case_id, "status": "skipped", "reason": "skip_agent=true in TEST.md"}

    if not trigger:
        return {"id": case_id, "status": "skipped", "reason": "empty trigger"}

    # Get agent/LLM response
    t0 = time.time()
    try:
        if backend == "openclaw":
            response = _trigger_openclaw_agent(probe, trigger, timeout=timeout)
        else:
            response = simulate_skill_response(
                skill_md_content=skill_md,
                trigger=trigger,
                cfg=cfg,
                timeout=timeout,
            )
    except TimeoutError as e:
        return {
            "id": case_id, "status": "timeout",
            "elapsed": round(time.time() - t0, 1),
            "error": str(e)[:300],
        }
    except Exception as e:
        return {
            "id": case_id, "status": "error",
            "elapsed": round(time.time() - t0, 1),
            "error": f"{type(e).__name__}: {e}"[:300],
        }

    # Score
    try:
        score, reason = score_response(
            response=response, expected=expected, case_input=trigger, cfg=cfg, timeout=60,
        )
    except Exception as e:
        return {
            "id": case_id, "status": "scoring_error",
            "response": response[:1000],
            "elapsed": round(time.time() - t0, 1),
            "error": f"{type(e).__name__}: {e}"[:300],
        }

    status = "pass" if score >= threshold else "fail"
    return {
        "id": case_id,
        "status": status,
        "score": round(score, 2),
        "threshold": threshold,
        "reason": reason,
        "response": response[:2000],
        "elapsed": round(time.time() - t0, 1),
    }


def main():
    args = parse_args()
    space_dir = os.path.expanduser(args.space_dir)

    # Load cases
    with open(args.cases) as f:
        cases_data = json.load(f)
    cases = cases_data.get("cases", [])
    skill_dir = cases_data.get("skill_dir", "")

    # Filter
    if args.cases_filter:
        wanted = set(args.cases_filter.split(","))
        cases = [c for c in cases if c.get("id") in wanted]

    if args.skip:
        results = [{"id": c.get("id"), "status": "skipped", "reason": "--skip-agent"} for c in cases]
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2))
        print(f"  → Skipped {len(results)} cases")
        return

    # Resolve config
    cli_args = {}
    if args.backend:
        cli_args["SR_BACKEND"] = args.backend
    cfg = resolve_config(cli_args=cli_args, project_dir=Path(skill_dir).parent if skill_dir else None)
    cfg = require_config_ready(cfg)
    backend = cfg["SR_BACKEND"]

    print(f"  → Backend: {backend} | Model: {cfg.get('SR_LLM_MODEL')} | Threshold: {args.threshold}", file=sys.stderr)

    # Prepare backend-specific resources
    probe = {}
    if backend == "openclaw":
        if not _openclaw_available():
            print("❌ Backend=openclaw but 'openclaw' CLI not found. Set SR_BACKEND=api or install OpenClaw.", file=sys.stderr)
            sys.exit(2)
        probe = _ensure_probe_job(space_dir, cfg["SR_TARGET_AGENT"])

    # Read SKILL.md (needed for api backend system prompt)
    skill_md = ""
    if skill_dir:
        skill_md_path = Path(skill_dir) / "SKILL.md"
        if skill_md_path.exists():
            skill_md = skill_md_path.read_text(encoding="utf-8")

    # Execute cases
    results = []
    hard_timeout = args.timeout + HARD_CASE_TIMEOUT_BUFFER
    for c in cases:
        case_id = c.get("id", "?")
        case_name = c.get("name", "")
        print(f"  ⏳ [{case_id}] {case_name}", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(
                _run_one_case, c, backend, cfg, probe, args.threshold, args.timeout, skill_md,
            )
            try:
                r = fut.result(timeout=hard_timeout)
            except FutureTimeout:
                r = {"id": case_id, "status": "timeout", "error": f"hard timeout {hard_timeout}s"}
        marker = {"pass": "✅", "fail": "❌", "timeout": "⏰", "error": "💥", "skipped": "⏭️", "scoring_error": "💥"}.get(r.get("status"), "?")
        score_str = f" score={r.get('score', '-')}" if "score" in r else ""
        print(f"     {marker} {r.get('status')}{score_str}", file=sys.stderr)
        results.append(r)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps({"backend": backend, "model": cfg.get("SR_LLM_MODEL"), "results": results}, ensure_ascii=False, indent=2),
    )
    print(f"  → Results saved: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
