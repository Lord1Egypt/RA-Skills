#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import complete_external_study as study


RETRYABLE_SOURCE_ERRORS = (
    "canonical_url was already used recently",
    "choose a different random live source",
    "No video formats found",
    "download_source",
    "command failed",
)


def log(message: str) -> None:
    print(message, flush=True)


def script_path(name: str) -> Path:
    return Path(__file__).resolve().parent / name


def run_json(cmd: list[str], timeout: int) -> dict[str, Any]:
    log("$ " + " ".join(shlex.quote(part) for part in cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    if proc.stderr.strip():
        log(proc.stderr.strip()[-4000:])
    if proc.returncode != 0:
        if proc.stdout.strip():
            try:
                return json.loads(proc.stdout)
            except Exception:
                pass
        raise RuntimeError((proc.stderr or proc.stdout or f"command failed: {proc.returncode}").strip())
    return json.loads(proc.stdout)


def picker_payload(platform: str, candidate_count: int, verify_limit: int, timeout: int) -> dict[str, Any]:
    return run_json(
        [
            sys.executable,
            str(script_path("pick_live_source.py")),
            "--platform",
            platform,
            "--candidate-count",
            str(candidate_count),
            "--verify-limit",
            str(verify_limit),
        ],
        timeout=timeout,
    )


def candidate_order(payload: dict[str, Any]) -> list[tuple[int, str]]:
    candidates = payload.get("candidates") if isinstance(payload.get("candidates"), list) else []
    out: list[tuple[int, str]] = []
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            continue
        url = str(item.get("url") or item.get("canonical_url") or "").strip()
        if url:
            out.append((index, url))
    selected = payload.get("selected_index")
    rng = random.SystemRandom()
    if isinstance(selected, int):
        preferred = [item for item in out if item[0] == selected]
        rest = [item for item in out if item[0] != selected]
        rng.shuffle(rest)
        return preferred + rest
    rng.shuffle(out)
    return out


def helper_attempt(workspace: Path, candidate_count: int, selected_index: int, url: str, timeout: int) -> tuple[int, str]:
    cmd = [
        sys.executable,
        str(script_path("complete_external_study.py")),
        "--workspace",
        str(workspace),
        "--candidate-count",
        str(candidate_count),
        "--selected-index",
        str(selected_index),
        "--url",
        url,
    ]
    log("$ " + " ".join(shlex.quote(part) for part in cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    text = (proc.stdout or "") + (proc.stderr or "")
    if text.strip():
        log(text.strip()[-6000:])
    return proc.returncode, text


def retryable(text: str) -> bool:
    lowered = text.lower()
    return any(item.lower() in lowered for item in RETRYABLE_SOURCE_ERRORS)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pick a random live source and complete external study, retrying alternate live candidates on duplicate/dead-source failures."
    )
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--candidate-count", type=int, default=8)
    parser.add_argument("--verify-limit", type=int, default=50)
    parser.add_argument("--picker-rounds", type=int, default=2)
    parser.add_argument("--max-helper-attempts", type=int, default=8)
    parser.add_argument("--helper-timeout", type=int, default=260)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    creds = study.load_credentials(workspace)
    home = study.fetch_home(creds["api_key"])
    action = study.choose_live_external_action(home)
    constraints = action.get("field_constraints") if isinstance(action.get("field_constraints"), dict) else {}
    platform = (
        constraints.get("required_source_platform")
        or (home.get("external_study_strategy") or {}).get("required_source_platform")
    )
    if not isinstance(platform, str) or not platform.strip():
        print("FAILED:missing_required_source_platform")
        return 2
    platform = platform.strip()
    last_error = ""
    tried: set[str] = set()
    for round_index in range(max(1, args.picker_rounds)):
        try:
            pick = picker_payload(platform, args.candidate_count, args.verify_limit, timeout=max(90, args.helper_timeout))
        except Exception as exc:
            last_error = f"picker_exception:{exc}"
            log(last_error)
            continue
        if not pick.get("ok"):
            last_error = "picker_failed:" + json.dumps(pick, ensure_ascii=False)
            log(last_error[-4000:])
            continue
        count = int(pick.get("candidate_count") or len(pick.get("candidates") or []) or 1)
        attempts = 0
        for selected_index, url in candidate_order(pick):
            if url in tried:
                continue
            tried.add(url)
            attempts += 1
            code, text = helper_attempt(workspace, count, selected_index, url, timeout=args.helper_timeout)
            if code == 0:
                print(
                    json.dumps(
                        {
                            "ok": True,
                            "platform": platform,
                            "round": round_index,
                            "selected_index": selected_index,
                            "canonical_url": url,
                            "tried_count": len(tried),
                        },
                        ensure_ascii=False,
                    )
                )
                return 0
            last_error = text.strip()[-2000:]
            if attempts >= args.max_helper_attempts:
                break
            if retryable(text):
                log("RETRYING_WITH_NEXT_RANDOM_LIVE_CANDIDATE")
                continue
            # Non-source contract failures should be visible; retrying another
            # URL would hide a real schema/auth/session problem.
            print("FAILED:external_study_helper_contract_error")
            print(last_error)
            return code or 2
        time.sleep(1)
    print("FAILED:external_study_all_random_candidates_failed")
    if last_error:
        print(last_error)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
