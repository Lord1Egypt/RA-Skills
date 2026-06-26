#!/usr/bin/env python3
"""
round-controller.py — orchestration skeleton for one round of structured deliberation.

This is a REFERENCE IMPLEMENTATION SKELETON. Adapt to your LLM API / harness.

The skeleton covers Phases A-H of a single round:
- Phase A: Lead assignment
- Phase B: Lead proposal generation
- Phase C: Supplements from non-lead agents
- Phase D: 4 artifacts produced (parallelizable)
- Phase E: 4 verifications (depends on Phase D)
- Phase F: Claims update + validation
- Phase G: Assessment / decision recording
- Phase H: (every K rounds) Drift check

The skeleton uses stub `call_llm()` / `extract_claims_from_artifacts()` / `run_verification_check()`
functions. Replace with your actual integrations.

Usage:
    python round-controller.py --round N --config config/ --state state/ --output artifacts/round_N/
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================
# STUBS — replace these with your actual integrations
# ============================================================

def call_llm(system_prompt: str, user_prompt: str, model: str = "claude-opus-4-7") -> str:
    """STUB: replace with actual LLM API call (Anthropic / OpenAI / etc.)."""
    raise NotImplementedError("Replace with your LLM API integration.")


def extract_claims_from_artifacts(artifacts: Dict[str, str], round_num: int) -> List[Dict]:
    """STUB: parse claims from artifact markdown. Returns list of claim dicts.

    Each claim should have: id, round, raised_by, text, testable_as, status (default 'pending').
    """
    raise NotImplementedError("Implement claim extraction by parsing the markdown 'Claims raised' sections.")


def run_verification_check(check: str, artifacts: Dict[str, str], state_dir: Path, round_num: int) -> Dict:
    """STUB: implement actual cross-validation logic per check.

    See references/verification-protocol.md for the procedure for each of the 4 checks.
    Should return a verifications.jsonl entry with id, round, check, result, evidence_refs, notes,
    claims_affected, claim_status_changes.
    """
    raise NotImplementedError(f"Implement verification logic for {check}")


# ============================================================
# Helpers
# ============================================================

def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    entries = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def append_jsonl(path: Path, entry: Dict):
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + "\n")


def render_template(template: str, variables: Dict[str, str]) -> str:
    """Naive template substitution. For production use Jinja2 or similar."""
    result = template
    for key, val in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(val))
    return result


def is_check_blocked_by_absence(check: str, absent: Optional[str]) -> bool:
    """Determine if a verification check is structurally impossible given the absent agent."""
    if not absent:
        return False
    blocking = {
        "critic_attack_on_action_trace": ("action", "critic"),
        "guardian_vs_observer_walkthrough": ("guardian", "observer"),
        "observer_friction_vs_critic_attack": ("observer", "critic"),
        "all_vs_prior_decisions": (),  # always applicable (uses all available artifacts)
    }
    return absent in blocking.get(check, ())


# ============================================================
# Phase implementations
# ============================================================

def phase_a_lead_assignment(round_num: int, lead_history: List[Dict], agent_names: List[str], stress_agent: Optional[str] = None) -> Dict:
    """Determine who leads this round (rotation by least-led)."""
    led_counts = {name: 0 for name in agent_names}
    for entry in lead_history:
        if entry.get("lead") in led_counts:
            led_counts[entry["lead"]] += 1

    candidates = [n for n in agent_names if n != stress_agent]
    lead = min(candidates, key=lambda n: led_counts[n])

    return {
        "round": round_num,
        "lead": lead,
        "is_stress": stress_agent is not None,
        "absent_agent": stress_agent,
    }


def phase_b_lead_proposal(round_num: int, lead: str, focus: str, prior_decisions: str, role_prompt: str, domain: str) -> str:
    """Lead agent writes the round proposal."""
    system = render_template(role_prompt, {
        "domain": domain,
        "round_focus": focus,
        "prior_decisions_summary": prior_decisions,
        "round_number": str(round_num),
    })
    user = f"Write the round {round_num} lead proposal (600-800 words). Focus: {focus}"
    return call_llm(system, user)


def phase_c_supplements(round_num: int, focus: str, lead_proposal: str, non_lead_agents: List[str], role_prompts: Dict[str, str], domain: str) -> Dict[str, str]:
    """Each non-lead, non-stressed agent writes a supplement."""
    supplements = {}
    for agent in non_lead_agents:
        system = render_template(role_prompts[agent], {
            "domain": domain,
            "round_number": str(round_num),
            "round_focus": focus,
            "prior_decisions_summary": "",
        })
        user = f"The round lead proposed:\n\n{lead_proposal}\n\nWrite your {agent} supplement (200-400 words)."
        supplements[agent] = call_llm(system, user)
    return supplements


def phase_d_artifacts(round_num: int, focus: str, agents: List[str], role_prompts: Dict[str, str], output_dir: Path, domain: str) -> Dict[str, str]:
    """Each non-stressed agent produces a structured artifact."""
    artifacts = {}
    output_dir.mkdir(parents=True, exist_ok=True)
    for agent in agents:
        system = render_template(role_prompts[agent], {
            "domain": domain,
            "round_number": str(round_num),
            "round_focus": focus,
            "prior_decisions_summary": "",
        })
        user = f"Produce your structured artifact for R{round_num}, following the schema in templates/artifact-schemas/{agent}.md.tmpl"
        artifact = call_llm(system, user)
        artifact_path = output_dir / f"{agent}.md"
        artifact_path.write_text(artifact, encoding='utf-8')
        artifacts[agent] = artifact
    return artifacts


def phase_e_verifications(round_num: int, artifacts: Dict[str, str], state_dir: Path, stress_agent: Optional[str] = None) -> List[Dict]:
    """Run 4 cross-validation checks."""
    checks = [
        "critic_attack_on_action_trace",
        "guardian_vs_observer_walkthrough",
        "observer_friction_vs_critic_attack",
        "all_vs_prior_decisions",
    ]

    verifications = []
    for i, check in enumerate(checks, 1):
        if is_check_blocked_by_absence(check, stress_agent):
            v = {
                "id": f"V-{round_num}-{i}",
                "round": round_num,
                "check": check,
                "result": "NOT_APPLICABLE",
                "evidence_refs": [],
                "notes": f"stress test: {stress_agent} absent",
                "claims_affected": [],
                "claim_status_changes": [],
            }
        else:
            v = run_verification_check(check, artifacts, state_dir, round_num)
        verifications.append(v)
        append_jsonl(state_dir / "verifications.jsonl", v)

    return verifications


def phase_f_claims_update(round_num: int, artifacts: Dict[str, str], verifications: List[Dict], state_dir: Path):
    """Append new claims, apply status changes, run validator."""
    new_claims = extract_claims_from_artifacts(artifacts, round_num)
    for claim in new_claims:
        append_jsonl(state_dir / "claims.jsonl", claim)

    # Status changes are recorded in verifications.jsonl already (claim_status_changes field).
    # Some implementations also write a separate status-update entry to claims.jsonl;
    # this skeleton treats verifications.jsonl as the source of truth for status transitions.

    # Run validator
    import subprocess
    script_path = Path(__file__).parent / "claims-validator.py"
    result = subprocess.run(
        ["python", str(script_path), "--state-dir", str(state_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claims validation failed:\n{result.stderr}")


def phase_g_assessment(round_num: int, lead_proposal: str, verifications: List[Dict], state_dir: Path) -> List[Dict]:
    """Record decisions made this round. Each decision must cite ≥1 claim or verification."""
    # STUB: extract decisions from lead_proposal + verification verdicts
    # This is domain-specific; here we just demonstrate the schema.
    decisions = []
    # ... user implementation ...

    for d in decisions:
        if not d.get("cites"):
            raise ValueError(f"decision {d.get('id')} has no citations — required by phase G")
        append_jsonl(state_dir / "decisions.jsonl", d)

    return decisions


def phase_h_drift_check(round_num: int, drift_check_every: int, anchor_path: Path, current_state: str) -> Optional[Dict]:
    """Run drift check if this round is on the K-round interval."""
    if round_num % drift_check_every != 0:
        return None

    # STUB: compare current state against anchor
    # Returns a verdict dict: {"verdict": "PASS|FAIL|PARTIAL", "deviation_score": 1-5, "notes": "..."}
    raise NotImplementedError("Implement drift check comparison logic.")


# ============================================================
# Main orchestration
# ============================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--config", type=Path, required=True, help="Config directory with role prompts and round_focus")
    parser.add_argument("--state", type=Path, required=True, help="State directory with jsonl files")
    parser.add_argument("--output", type=Path, required=True, help="Artifacts output directory for this round")
    parser.add_argument("--stress-agent", type=str, default=None, help="Agent to stress-test (forced absent)")
    parser.add_argument("--drift-check-every", type=int, default=5)
    parser.add_argument("--domain", type=str, required=True, help="Problem domain string for prompts")
    parser.add_argument("--focus", type=str, required=True, help="Round focus question")
    args = parser.parse_args()

    agent_names = ["action", "guardian", "observer", "critic"]

    # Load role prompt templates from config
    role_prompts = {}
    for agent in agent_names:
        prompt_path = args.config / f"role-prompts/{agent}.txt"
        if prompt_path.exists():
            role_prompts[agent] = prompt_path.read_text(encoding='utf-8')
        else:
            # Fallback: extract from templates/role-prompt.md.tmpl
            role_prompts[agent] = f"<configure {agent} prompt in {prompt_path}>"

    lead_history = load_jsonl(args.state / "lead_history.jsonl")
    prior_decisions_summary = ""  # populate from decisions.jsonl as needed

    # Phase A
    assignment = phase_a_lead_assignment(args.round, lead_history, agent_names, args.stress_agent)
    print(f"Phase A — Lead: {assignment['lead']}, stress: {assignment['absent_agent']}")
    append_jsonl(args.state / "lead_history.jsonl", assignment)

    active_agents = [a for a in agent_names if a != args.stress_agent]
    non_lead_active = [a for a in active_agents if a != assignment["lead"]]

    # Phase B
    lead_proposal = phase_b_lead_proposal(
        args.round, assignment["lead"], args.focus, prior_decisions_summary,
        role_prompts[assignment["lead"]], args.domain,
    )
    print("Phase B — lead proposal generated")

    # Phase C
    supplements = phase_c_supplements(args.round, args.focus, lead_proposal, non_lead_active, role_prompts, args.domain)
    print(f"Phase C — supplements from {list(supplements.keys())}")

    # Phase D
    artifacts = phase_d_artifacts(args.round, args.focus, active_agents, role_prompts, args.output, args.domain)
    print(f"Phase D — artifacts: {list(artifacts.keys())}")

    # Phase E
    verifications = phase_e_verifications(args.round, artifacts, args.state, args.stress_agent)
    print(f"Phase E — {len(verifications)} verifications")

    # Phase F
    phase_f_claims_update(args.round, artifacts, verifications, args.state)
    print("Phase F — claims updated and validated")

    # Phase G
    decisions = phase_g_assessment(args.round, lead_proposal, verifications, args.state)
    print(f"Phase G — {len(decisions)} decisions recorded")

    # Phase H
    drift_result = phase_h_drift_check(args.round, args.drift_check_every, args.config / "product_anchor.md", "")
    if drift_result:
        print(f"Phase H — drift check: {drift_result['verdict']}")

    print(f"\nRound {args.round} complete.")


if __name__ == "__main__":
    main()
