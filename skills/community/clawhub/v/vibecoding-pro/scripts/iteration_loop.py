"""
DoubleAgent Iteration Loop — Template Implementation
=====================================================
This script provides a complete framework for running a Generator-Evaluator
dual-agent loop. Adapt the `run_generator` and `run_evaluator` functions
to your specific agent setup (WorkBuddy subagents, API calls, etc.)

Usage:
    python iteration_loop.py --spec spec.md --url http://localhost:3000 --rounds 15 --threshold 85
"""

import json
import argparse
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


# ─── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class ScoreBreakdown:
    functional_completeness: int = 0   # /30
    interaction_quality: int = 0       # /25
    edge_case_handling: int = 0        # /20
    code_design_quality: int = 0       # /15
    craft_originality: int = 0         # /10

    @property
    def total(self) -> int:
        return (
            self.functional_completeness +
            self.interaction_quality +
            self.edge_case_handling +
            self.code_design_quality +
            self.craft_originality
        )


@dataclass
class EvaluationResult:
    round: int
    total_score: int
    score_breakdown: ScoreBreakdown
    requirement_results: list = field(default_factory=list)
    critical_failures: list = field(default_factory=list)
    recommendation: str = "continue"   # continue|switch_approach|accept|escalate
    evaluator_note: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class IterationHistory:
    rounds: list = field(default_factory=list)  # list of EvaluationResult
    approach_switches: int = 0
    best_score: int = 0
    best_round: int = 0

    def add(self, result: EvaluationResult):
        self.rounds.append(result)
        if result.total_score > self.best_score:
            self.best_score = result.total_score
            self.best_round = result.round

    @property
    def trend(self) -> str:
        """Compute score trend from last 3 rounds."""
        if len(self.rounds) < 3:
            return "improving"
        recent = [r.total_score for r in self.rounds[-3:]]
        delta = recent[-1] - recent[0]
        if delta > 5:
            return "improving"
        elif delta < -5:
            return "degrading"
        else:
            return "plateauing"

    def to_summary(self) -> dict:
        return {
            "rounds_completed": len(self.rounds),
            "best_score": self.best_score,
            "best_round": self.best_round,
            "current_score": self.rounds[-1].total_score if self.rounds else 0,
            "trend": self.trend,
            "approach_switches": self.approach_switches,
            "scores_per_round": [r.total_score for r in self.rounds]
        }


# ─── Agent Interface (adapt these to your actual agent setup) ─────────────────

def run_generator(
    spec: str,
    history: IterationHistory,
    switch_approach: bool = False,
    **kwargs
) -> dict:
    """
    Run the Generator agent to produce/improve an artifact.
    
    ADAPT THIS: In WorkBuddy, this would call the `coder` subagent.
    In API setups, this would call Claude/GPT with the generator system prompt.
    
    Returns:
        dict with keys: artifact_url, summary, approach_used
    """
    print(f"\n[Generator] Round {len(history.rounds) + 1}")
    if switch_approach:
        print("[Generator] ⚡ Switching approach based on evaluator feedback")
    
    history_summary = history.to_summary() if history.rounds else {}
    last_feedback = history.rounds[-1] if history.rounds else None
    
    # ─── REPLACE THIS BLOCK with actual generator call ───────────────────────
    # Example WorkBuddy subagent call:
    # result = sessions_spawn(
    #     agentId="coder",
    #     runtime="subagent",
    #     task=f"""
    #     Implement the following spec: {spec}
    #     
    #     {'IMPORTANT: Switch to a completely different approach. Previous approach scored only '
    #       + str(last_feedback.total_score) + '/100' if switch_approach else ''}
    #     
    #     Previous evaluation feedback:
    #     {json.dumps(asdict(last_feedback), indent=2) if last_feedback else 'First round'}
    #     
    #     Deploy to localhost and return the URL.
    #     """
    # )
    # ─────────────────────────────────────────────────────────────────────────
    
    raise NotImplementedError(
        "Implement run_generator() with your actual agent setup.\n"
        "See comments above for WorkBuddy subagent example."
    )


def run_evaluator(
    spec: str,
    artifact_url: str,
    round_num: int,
    history: IterationHistory,
    **kwargs
) -> EvaluationResult:
    """
    Run the Evaluator agent to score the artifact.
    
    ADAPT THIS: In WorkBuddy, this would call the `tester` subagent with Playwright.
    The Evaluator reads the SPEC, opens the URL, interacts like a user, then scores.
    
    Returns:
        EvaluationResult with structured scores and feedback
    """
    print(f"\n[Evaluator] Evaluating round {round_num} artifact at {artifact_url}")
    
    # ─── REPLACE THIS BLOCK with actual evaluator call ───────────────────────
    # Example WorkBuddy tester subagent call:
    # result = sessions_spawn(
    #     agentId="tester",
    #     runtime="subagent",
    #     task=f"""
    #     [SYSTEM: You are an independent QA Evaluator. Do NOT generate code.]
    #     
    #     Spec (source of truth): {spec}
    #     Artifact URL: {artifact_url}
    #     Round: {round_num}
    #     
    #     1. Open {artifact_url} using Playwright
    #     2. Execute each test scenario from the spec as a real user
    #     3. Take screenshots of key interactions
    #     4. Score using this rubric:
    #        - functional_completeness: /30
    #        - interaction_quality: /25
    #        - edge_case_handling: /20
    #        - code_design_quality: /15
    #        - craft_originality: /10
    #     5. Return ONLY JSON matching EvaluationResult schema
    #     
    #     CALIBRATION: 50=mediocre, 80=good, 95=excellent
    #     """
    # )
    # ─────────────────────────────────────────────────────────────────────────
    
    raise NotImplementedError(
        "Implement run_evaluator() with your actual agent setup.\n"
        "See comments above for WorkBuddy tester subagent example."
    )


# ─── Main Loop ────────────────────────────────────────────────────────────────

def run_double_agent_loop(
    spec: str,
    pass_threshold: int = 85,
    max_rounds: int = 15,
    plateau_switch_threshold: int = 3,  # Switch approach after N plateauing rounds
    max_approach_switches: int = 3,     # Escalate after this many switches
    output_log: Optional[str] = None,
    **kwargs
) -> dict:
    """
    Main Generator-Evaluator iteration loop.
    
    Args:
        spec: The specification document (full text)
        pass_threshold: Score at which to accept and exit (0-100)
        max_rounds: Maximum iterations before forced exit
        plateau_switch_threshold: Rounds of plateau before switching approach
        max_approach_switches: Times to switch before escalating to human
        output_log: Path to write iteration log JSON
    
    Returns:
        dict with final result, history, and recommendation
    """
    history = IterationHistory()
    plateau_count = 0
    
    print(f"🚀 Starting DoubleAgent loop")
    print(f"   Pass threshold: {pass_threshold}/100")
    print(f"   Max rounds: {max_rounds}")
    print("=" * 60)
    
    for round_num in range(1, max_rounds + 1):
        print(f"\n{'='*20} ROUND {round_num}/{max_rounds} {'='*20}")
        
        # Determine if we should switch approach
        should_switch = (
            history.trend == "plateauing" and
            plateau_count >= plateau_switch_threshold
        )
        
        # Check escalation condition
        if history.approach_switches >= max_approach_switches:
            print(f"⚠️  Reached max approach switches ({max_approach_switches}). Escalating.")
            result = {
                "status": "escalated",
                "reason": "max_approach_switches_reached",
                "best_score": history.best_score,
                "best_round": history.best_round,
                "history": history.to_summary(),
                "recommendation": "Requires human review and intervention"
            }
            _save_log(result, output_log)
            return result
        
        # Run Generator
        try:
            gen_result = run_generator(spec, history, switch_approach=should_switch, **kwargs)
            artifact_url = gen_result["artifact_url"]
            
            if should_switch:
                history.approach_switches += 1
                plateau_count = 0
                print(f"   Approach switch #{history.approach_switches}: {gen_result.get('approach_used', 'unknown')}")
        
        except Exception as e:
            print(f"❌ Generator failed: {e}")
            break
        
        # Run Evaluator
        try:
            eval_result = run_evaluator(spec, artifact_url, round_num, history, **kwargs)
            history.add(eval_result)
        
        except Exception as e:
            print(f"❌ Evaluator failed: {e}")
            break
        
        # Report round results
        print(f"\n📊 Round {round_num} Score: {eval_result.total_score}/100")
        print(f"   Breakdown: FC={eval_result.score_breakdown.functional_completeness}/30 "
              f"IQ={eval_result.score_breakdown.interaction_quality}/25 "
              f"EC={eval_result.score_breakdown.edge_case_handling}/20 "
              f"CQ={eval_result.score_breakdown.code_design_quality}/15 "
              f"OR={eval_result.score_breakdown.craft_originality}/10")
        print(f"   Note: {eval_result.evaluator_note}")
        print(f"   Trend: {history.trend}")
        
        # Check exit conditions
        if eval_result.total_score >= pass_threshold:
            print(f"\n✅ PASSED! Score {eval_result.total_score} ≥ threshold {pass_threshold}")
            result = {
                "status": "passed",
                "final_score": eval_result.total_score,
                "rounds_taken": round_num,
                "artifact_url": artifact_url,
                "history": history.to_summary()
            }
            _save_log(result, output_log)
            return result
        
        if eval_result.recommendation == "escalate":
            print(f"\n⚠️  Evaluator recommends escalation. Stopping loop.")
            result = {
                "status": "escalated",
                "reason": "evaluator_recommendation",
                "score": eval_result.total_score,
                "evaluator_note": eval_result.evaluator_note,
                "history": history.to_summary()
            }
            _save_log(result, output_log)
            return result
        
        # Update plateau counter
        if history.trend == "plateauing":
            plateau_count += 1
        else:
            plateau_count = 0
    
    # Max rounds reached
    print(f"\n⏱️  Max rounds ({max_rounds}) reached. Best score: {history.best_score}/100")
    result = {
        "status": "max_rounds_reached",
        "best_score": history.best_score,
        "best_round": history.best_round,
        "rounds_taken": max_rounds,
        "passed_threshold": history.best_score >= pass_threshold,
        "history": history.to_summary(),
        "recommendation": "accept" if history.best_score >= (pass_threshold - 10) else "human_review"
    }
    _save_log(result, output_log)
    return result


def _save_log(result: dict, output_log: Optional[str]):
    if output_log:
        with open(output_log, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📝 Log saved to {output_log}")


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DoubleAgent Iteration Loop")
    parser.add_argument("--spec", required=True, help="Path to spec file or spec text")
    parser.add_argument("--url", default=None, help="Initial artifact URL (if already deployed)")
    parser.add_argument("--threshold", type=int, default=85, help="Pass threshold (0-100)")
    parser.add_argument("--rounds", type=int, default=15, help="Max rounds")
    parser.add_argument("--log", default=None, help="Output log file path")
    args = parser.parse_args()
    
    # Load spec
    try:
        with open(args.spec, 'r', encoding='utf-8') as f:
            spec_content = f.read()
    except FileNotFoundError:
        spec_content = args.spec  # Treat as inline spec text
    
    result = run_double_agent_loop(
        spec=spec_content,
        pass_threshold=args.threshold,
        max_rounds=args.rounds,
        output_log=args.log,
        initial_url=args.url
    )
    
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: {result['status'].upper()}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
