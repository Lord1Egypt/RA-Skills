# -*- coding: utf-8 -*-
"""
skill-evolve-pro Phase 6
skill_scheduler.py - Scheduler (wires Phase 1-5 into full pipeline)

Pipeline:
  1. load_state -> get current evolution state
  2. skill_reflect.reflect() -> generate edits from trajectories
  3. skill_apply.apply_all_edits() -> apply edits, produce skill_after
  4. skill_gate.gate_validate() -> validate (auto or manual)
  5. If gate passes -> write skill file -> bump_round -> record_edits -> save_state
"""

from __future__ import annotations

import json as _json
import os
import sys
import glob as _glob
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Phase 1-5 imports
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from state_manager import (
    EvolveState, load_state, save_state, bump_round,
    record_edits, update_trajectory_stats, init_state,
)
from skill_reflect import reflect
from skill_apply import apply_all_edits
from skill_gate import gate_validate, GateResult
from trajectory_loader import (
    load_failed_trajectories, load_from_session_state,
    load_rollout_from_json,
)

# Path config（优先读取 config.py，其次环境变量）────────────────────────
try:
    from config import WORKSPACE, DEFAULT_SESSION, DEFAULT_TEMP, DEFAULT_ROLLOUT
except ImportError:
    import os
    WORKSPACE = Path(os.environ.get(
        "OPENCLAW_WORKSPACE",
        os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
    ))
    DEFAULT_SESSION = WORKSPACE / "SESSION-STATE.md"
    DEFAULT_TEMP = WORKSPACE / "temp"
    DEFAULT_ROLLOUT = WORKSPACE / "temp" / "rollouts"


@dataclass
class RunResult:
    """Result of run_full_cycle()."""
    skill_before: str = ""
    skill_after: str = ""
    edits: list = field(default_factory=list)
    gate_result: Optional[GateResult] = None
    applied_count: int = 0
    rejected_count: int = 0
    new_state: Optional[EvolveState] = None
    reflect_reasoning: str = ""
    reflect_summary: str = ""

    def to_dict(self) -> dict:
        return {
            "edits_count": len(self.edits),
            "gate_passed": self.gate_result.passed if self.gate_result else False,
            "applied_count": self.applied_count,
            "rejected_count": self.rejected_count,
            "new_state": asdict(self.new_state) if self.new_state else None,
        }


def run_full_cycle(
    skill_id: str,
    skill_content: str,
    rollouts: list,
    max_edits: int = 8,
    auto_gate: bool = True,
    skill_version: str = "1.0.0",
) -> RunResult:
    """
    Execute full SkillOpt evolution cycle.

    Pipeline:
    1. load_state -> get current state (init if not exists)
    2. round += 1
    3. update trajectory stats
    4. skill_reflect.reflect() -> generate edits
    5. skill_apply.apply_all_edits() -> apply edits, produce skill_after
    6. skill_gate.gate_validate() -> validate edits
    7. If gate passes -> record_edits -> save_state
       If gate fails -> keep skill_before -> save_state
    """
    # Step 1: load or init state
    state = load_state(skill_id)
    if state is None:
        state = init_state(skill_id, skill_version, edit_budget=max_edits)

    skill_before = skill_content

    # Step 2: bump round
    state.round += 1
    state.last_update = datetime.now().isoformat()

    # Step 3: update trajectory stats
    hard_success = sum(1 for r in rollouts if float(getattr(r, "hard", 0)) >= 1.0)
    hard_fail = sum(1 for r in rollouts if float(getattr(r, "hard", 0)) < 1.0)
    stats = state.trajectory_stats
    stats["total"] += len(rollouts)
    stats["hard_success"] += hard_success
    stats["hard_fail"] += hard_fail

    # Step 4: reflect
    print("\n[scheduler] Step 4/6 - calling reflect() ...")
    print(f"[scheduler]   rollouts: {len(rollouts)} (success={hard_success}, fail={hard_fail})")

    reflect_result = reflect(skill_content, rollouts)
    edits = reflect_result.get("edits", [])
    reflect_reasoning = reflect_result.get("reasoning", "")
    reflect_summary = reflect_result.get("summary", "")

    print(f"[scheduler]   reflect generated {len(edits)} edit suggestions")

    # Step 5: apply edits
    print("\n[scheduler] Step 5/6 - calling apply_all_edits() ...")
    print(f"[scheduler]   raw edits: {len(edits)}")

    skill_after, edit_reports = apply_all_edits(skill_content, edits)
    applied_reports = [r for r in edit_reports if r.get("status", "").startswith("applied")]
    applied_count = len(applied_reports)

    print(f"[scheduler]   applied: {applied_count}, skipped: {len(edit_reports) - applied_count}")

    # Step 6: gate validation
    print("\n[scheduler] Step 6/6 - calling gate_validate() ...")
    print(f"[scheduler]   auto_gate={auto_gate}")

    gate_result: GateResult = GateResult(passed=False)
    gate_passed = False

    if auto_gate:
        gate_result = gate_validate(
            skill_before=skill_before,
            skill_after=skill_after,
            edits=edits,
            rollouts=rollouts,
        )
        gate_passed = gate_result.passed
    else:
        gate_result = GateResult(
            passed=False,
            decisions=[],
            reasoning="Manual mode: auto validation skipped.",
        )

    if gate_passed and applied_count > 0:
        print("\n[scheduler] Gate PASSED - SKILL.md will be updated")
    else:
        print("\n[scheduler] Gate NOT passed - SKILL.md unchanged")
        skill_after = skill_before

    rejected_count = len(edit_reports) - applied_count

    state.edit_history.append({
        "round": state.round,
        "applied": applied_count,
        "rejected": rejected_count,
        "edits_count": len(edits),
        "gate_passed": gate_passed,
        "timestamp": datetime.now().isoformat(),
    })

    save_state(state)

    return RunResult(
        skill_before=skill_before,
        skill_after=skill_after,
        edits=edits,
        gate_result=gate_result,
        applied_count=applied_count,
        rejected_count=rejected_count,
        new_state=state,
        reflect_reasoning=reflect_reasoning,
        reflect_summary=reflect_summary,
    )


def load_rollouts_from_files(
    session_file: Optional[Path] = None,
    temp_dir: Optional[Path] = None,
    rollout_dir: Optional[Path] = None,
) -> list:
    """Load rollouts from multiple sources with deduplication."""
    all_rollouts = []
    session_file = session_file or DEFAULT_SESSION
    temp_dir = temp_dir or DEFAULT_TEMP
    rollout_dir = rollout_dir or DEFAULT_ROLLOUT

    if session_file and session_file.exists():
        try:
            rollouts = load_from_session_state(str(session_file))
            if rollouts:
                all_rollouts.extend([r.to_dict() if hasattr(r, "to_dict") else r for r in rollouts])
                print(f"[scheduler] Loaded {len(rollouts)} trajectories from SESSION-STATE.md")
        except Exception as e:
            print(f"[scheduler] SESSION-STATE.md parse failed: {e}")

    if rollout_dir and rollout_dir.exists():
        for fpath in sorted(_glob.glob(str(rollout_dir / "rollout_*.json"))):
            try:
                rollouts = load_rollout_from_json(fpath)
                all_rollouts.extend([r.to_dict() if hasattr(r, "to_dict") else r for r in rollouts])
            except Exception as e:
                print(f"[scheduler] rollout JSON parse failed: {e}")

    if temp_dir and temp_dir.exists():
        try:
            trajs = load_failed_trajectories(str(temp_dir))
            if trajs:
                all_rollouts.extend(trajs)
                print(f"[scheduler] Loaded {len(trajs)} failed trajectories from temp/")
        except Exception as e:
            print(f"[scheduler] temp/ load failed: {e}")

    # deduplicate by id
    seen = set()
    deduped = []
    for r in all_rollouts:
        rid = r.get("id", "")
        if rid not in seen:
            seen.add(rid)
            deduped.append(r)
    return deduped


def run_from_skill_dir(
    skill_dir: Path,
    max_edits: int = 8,
    auto_gate: bool = True,
) -> RunResult:
    """Load SKILL.md + rollouts from disk and run full evolution cycle."""
    skill_json_path = skill_dir / "skill.json"
    if skill_json_path.exists():
        skill_meta = _json.loads(skill_json_path.read_text(encoding="utf-8"))
        skill_id = skill_meta.get("name", skill_dir.name)
        skill_version = skill_meta.get("version", "1.0.0")
    else:
        skill_id = skill_dir.name
        skill_version = "1.0.0"

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    skill_content = skill_file.read_text(encoding="utf-8")

    rollouts = load_rollouts_from_files()

    return run_full_cycle(
        skill_id=skill_id,
        skill_content=skill_content,
        rollouts=rollouts,
        max_edits=max_edits,
        auto_gate=auto_gate,
        skill_version=skill_version,
    )


def format_cycle_report(result: RunResult) -> str:
    """Format evolution result as a Chinese-readable report."""
    lines = []

    lines.append("")
    lines.append("=" * 70)
    lines.append("  [Phase 6] skill-evolve-pro Evolution Report (进化报告)")
    lines.append("=" * 70)

    state = result.new_state
    if state:
        prev_round = state.round - 1
        lines.append("")
        lines.append("[Evolution State]")
        lines.append(f"  skill_id    : {state.skill_id}")
        lines.append(f"  version     : v{state.version}")
        lines.append(f"  epoch       : {state.epoch}")
        lines.append(f"  round       : {state.round}  (previous: {prev_round})")
        lines.append(f"  edit_budget : {state.edit_budget}")

        stats = state.trajectory_stats
        lines.append("")
        lines.append("[Trajectory Stats (cumulative)]")
        lines.append(f"  total        : {stats['total']} trajectories")
        lines.append(f"  hard_success : {stats['hard_success']}")
        lines.append(f"  hard_fail    : {stats['hard_fail']}")
        lines.append(f"  soft_fail    : {stats['soft_fail']}")

    lines.append("")
    lines.append("[Edits Generated]")
    lines.append(f"  {len(result.edits)} edit suggestions generated")

    for i, edit in enumerate(result.edits[:10], 1):
        op = edit.get("op", "unknown")
        target = edit.get("target", "")[:60]
        content = edit.get("content", "")[:80]
        priority = edit.get("priority", "medium")
        reason = edit.get("reason", "")
        fail_count = edit.get("fail_count", "")

        tag_map = {"high": "[HIGH]", "medium": "[MED]", "low": "[LOW]"}
        tag = tag_map.get(priority, "")
        lines.append(f"  Edit{i}: {tag} [{op.upper()}]")
        if target:
            lines.append(f"    target   : {repr(target)}")
        if content:
            lines.append(f"    content  : {repr(content)}")
        if reason:
            lines.append(f"    reason   : {reason}")
        if fail_count:
            lines.append(f"    fail_count: {fail_count}")

    if result.reflect_reasoning:
        lines.append("")
        lines.append("[Reflect Reasoning]")
        lines.append(f"  {result.reflect_reasoning[:400]}")

    if result.reflect_summary:
        lines.append("")
        lines.append("[Reflect Summary]")
        lines.append(f"  {result.reflect_summary[:400]}")

    lines.append("")
    lines.append("[Gate Validation]")
    gate = result.gate_result
    if gate:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"  Overall   : [{status}] {'passed' if gate.passed else 'not passed'}")
        lines.append(f"  Reasoning : {gate.reasoning[:200]}")
        if gate.concerns:
            lines.append(f"  Concerns ({len(gate.concerns)}):")
            for c in gate.concerns[:5]:
                lines.append(f"    - {c[:100]}")
        if gate.decisions:
            lines.append(f"  Per-edit decisions ({len(gate.decisions)}):")
            for d in gate.decisions:
                action = d.get("action", "unknown")
                idx = d.get("index", "?")
                op_d = d.get("op", "")
                reason_d = d.get("reason", "")[:60]
                lines.append(f"    [{idx}] {action:8s}  op={op_d:15s}  reason={reason_d}")
    else:
        lines.append("  [SKIP] validation was skipped")

    lines.append("")
    lines.append("[Apply Results]")
    lines.append(f"  applied     : {result.applied_count}")
    lines.append(f"  rejected/skip: {result.rejected_count}")

    if state and state.edit_history:
        last = state.edit_history[-1]
        lines.append("")
        lines.append("[State Update]")
        lines.append(f"  round bumped to: {state.round}")
        lines.append(f"  edit_history entries: {len(state.edit_history)}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


# ── CLI entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="skill_scheduler.py Phase 6 - evolution scheduler")
    parser.add_argument("--skill-dir", "-s", type=Path, default=None,
                        help="Skill directory containing SKILL.md")
    parser.add_argument("--skill-id", default="robot-evolve",
                        help="Skill ID")
    parser.add_argument("--skill-content", default=None,
                        help="SKILL.md content (overrides --skill-dir)")
    parser.add_argument("--rollouts", "-r", type=Path, default=None,
                        help="Rollout JSON file")
    parser.add_argument("--temp-dir", type=Path, default=None,
                        help="Temp directory with failed_trajectory_*.json files")
    parser.add_argument("--session-file", type=Path, default=None,
                        help="SESSION-STATE.md path")
    parser.add_argument("--max-edits", type=int, default=8,
                        help="Max edits (edit_budget)")
    parser.add_argument("--no-auto-gate", action="store_true",
                        help="Disable auto gate (manual mode)")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output file for updated SKILL.md")
    args = parser.parse_args()

    # Load skill content
    if args.skill_content:
        skill_content = args.skill_content
        skill_id = args.skill_id
        skill_version = "1.0.0"
    elif args.skill_dir:
        skill_dir = args.skill_dir
        skill_json = skill_dir / "skill.json"
        if skill_json.exists():
            meta = json.loads(skill_json.read_text(encoding="utf-8"))
            skill_id = meta.get("name", skill_dir.name)
            skill_version = meta.get("version", "1.0.0")
        else:
            skill_id = skill_dir.name
            skill_version = "1.0.0"
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            print(f"ERROR: SKILL.md not found in {skill_dir}")
            sys.exit(1)
        skill_content = skill_file.read_text(encoding="utf-8")
    else:
        # Default: robot-evolve skill
        # Default: robot-evolve skill
        try:
            from config import DEFAULT_TARGET_SKILL_DIR
            robot_evolve_dir = DEFAULT_TARGET_SKILL_DIR
        except ImportError:
            robot_evolve_dir = WORKSPACE / "skills" / "robot-evolve"
        skill_json = robot_evolve_dir / "skill.json"
        if skill_json.exists():
            meta = json.loads(skill_json.read_text(encoding="utf-8"))
            skill_id = meta.get("name", "robot-evolve")
            skill_version = meta.get("version", "3.0.3")
        else:
            skill_id = "robot-evolve"
            skill_version = "3.0.3"
        skill_file = robot_evolve_dir / "SKILL.md"
        skill_content = skill_file.read_text(encoding="utf-8")

    # Load rollouts
    if args.rollouts:
        rollouts = json.loads(args.rollouts.read_text(encoding="utf-8"))
        if not isinstance(rollouts, list):
            rollouts = [rollouts]
        print(f"[scheduler] Loaded {len(rollouts)} rollouts from {args.rollouts}")
    else:
        rollouts = load_rollouts_from_files(
            session_file=args.session_file,
            temp_dir=args.temp_dir,
        )
        if not rollouts:
            # Fallback: load trajectories_demo.json
            demo_path = WORKSPACE / "temp" / "trajectories_demo.json"
            if demo_path.exists():
                import json as _json2
                rollouts = _json2.loads(demo_path.read_text(encoding="utf-8"))
                if not isinstance(rollouts, list):
                    rollouts = [rollouts]
                print(f"[scheduler] Fallback: loaded {len(rollouts)} rollouts from trajectories_demo.json")
            else:
                rollouts = []
                print("[scheduler] WARNING: no rollouts found")

    auto_gate = not args.no_auto_gate

    print(f"[scheduler] Starting evolution cycle for skill={skill_id} v{skill_version}")
    print(f"[scheduler]   rollouts: {len(rollouts)}, auto_gate={auto_gate}")

    result = run_full_cycle(
        skill_id=skill_id,
        skill_content=skill_content,
        rollouts=rollouts,
        max_edits=args.max_edits,
        auto_gate=auto_gate,
        skill_version=skill_version,
    )

    report = format_cycle_report(result)
    print(report)

    gate_passed = result.gate_result and result.gate_result.passed
    if gate_passed and result.applied_count > 0:
        out_dir = args.skill_dir or robot_evolve_dir
        out_file = out_dir / "SKILL.md"
        out_file.write_text(result.skill_after, encoding="utf-8")
        print("")
        print(f"[scheduler] SKILL.md updated: {out_file}")
    else:
        print("")
        print("[scheduler] SKILL.md was NOT updated (gate did not pass)")

    if args.output:
        args.output.write_text(result.skill_after, encoding="utf-8")
        print(f"[scheduler] Output written to: {args.output}")

    print("")
    print("[scheduler] Done.")
