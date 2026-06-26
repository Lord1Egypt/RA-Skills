"""
DoubleAgent Evaluator Calibration Utility
==========================================
Run this BEFORE starting a production DoubleAgent loop to verify your
Evaluator's scoring is calibrated (not inflated/deflated).

Usage:
    python calibrate_evaluator.py --evaluator-config evaluator.json

The script runs the Evaluator on 4 known-quality examples and checks that
scores land within expected ranges. If they don't, it prints calibration advice.
"""

import json
import sys
from dataclasses import dataclass
from typing import Callable


# ─── Calibration Fixtures ─────────────────────────────────────────────────────

CALIBRATION_FIXTURES = [
    {
        "id": "CAL-A",
        "label": "Clearly broken (~30/100)",
        "description": """
            Web page loads but all CSS is missing (unstyled HTML).
            All buttons are present but clicking any produces a JavaScript error in console.
            The main form submits but returns HTTP 500.
            Navigation links exist but lead to 404 pages.
        """,
        "expected_min": 15,
        "expected_max": 40,
    },
    {
        "id": "CAL-B",
        "label": "Mediocre (~60/100)",
        "description": """
            Page renders with styles. Main navigation works correctly.
            Primary form submits successfully with valid data.
            No loading state shown during submission (spec requires one).
            Error messages are generic ("An error occurred") — spec requires specific messages.
            Mobile layout breaks below 375px width.
        """,
        "expected_min": 50,
        "expected_max": 70,
    },
    {
        "id": "CAL-C",
        "label": "Good (~85/100)",
        "description": """
            All spec requirements pass end-to-end.
            Navigation, forms, and primary flows work correctly.
            Mobile layout is responsive across 320px-1440px.
            Error messages match spec text exactly.
            Loading states shown correctly.
            Minor issue: hover state missing on one secondary CTA button.
            Edge case: empty list state shows generic message instead of spec-required illustration.
        """,
        "expected_min": 78,
        "expected_max": 92,
    },
    {
        "id": "CAL-D",
        "label": "Excellent (~95/100)",
        "description": """
            All spec requirements pass with zero regressions.
            All edge cases handled (empty states, errors, loading, boundary inputs).
            Custom animations match design spec exactly.
            Accessibility: all interactive elements have aria-labels.
            Performance: main bundle < 200KB gzipped (spec requires < 250KB).
            Mobile: pixel-perfect at 375px, 768px, 1280px.
            No console errors or warnings.
        """,
        "expected_min": 88,
        "expected_max": 100,
    },
]


# ─── Calibration Runner ───────────────────────────────────────────────────────

@dataclass
class CalibrationResult:
    fixture_id: str
    label: str
    expected_min: int
    expected_max: int
    actual_score: int
    passed: bool
    deviation: int


def run_calibration(
    evaluator_fn: Callable[[str], int],
    spec: str = "Generic web application spec",
    verbose: bool = True
) -> tuple[bool, list[CalibrationResult]]:
    """
    Run the Evaluator on all calibration fixtures and check results.
    
    Args:
        evaluator_fn: Function that takes artifact_description and returns score (0-100)
                      This should call your actual Evaluator agent.
        spec: The spec to use for calibration (use your real spec or a generic one)
        verbose: Print detailed results
    
    Returns:
        (all_passed, results) tuple
    """
    results = []
    
    if verbose:
        print("🎯 Running Evaluator Calibration")
        print("=" * 60)
    
    for fixture in CALIBRATION_FIXTURES:
        if verbose:
            print(f"\n[{fixture['id']}] {fixture['label']}")
            print(f"Expected: {fixture['expected_min']}-{fixture['expected_max']}/100")
        
        # ─── ADAPT THIS: Call your actual Evaluator ───────────────────────────
        # For WorkBuddy tester subagent:
        # actual_score = sessions_spawn(
        #     agentId="tester",
        #     runtime="subagent",
        #     task=f"""
        #     [CALIBRATION MODE]
        #     Spec: {spec}
        #     Artifact description (no URL available, evaluate from description):
        #     {fixture['description']}
        #     
        #     Score this artifact from 0-100 using the standard rubric.
        #     Return ONLY a JSON: {{"score": <number>}}
        #     """
        # )
        # actual_score = json.loads(actual_score)["score"]
        # ─────────────────────────────────────────────────────────────────────
        
        # Placeholder — replace with actual call
        actual_score = evaluator_fn(fixture["description"])
        
        passed = fixture["expected_min"] <= actual_score <= fixture["expected_max"]
        deviation = max(0, fixture["expected_min"] - actual_score) + max(0, actual_score - fixture["expected_max"])
        
        result = CalibrationResult(
            fixture_id=fixture["id"],
            label=fixture["label"],
            expected_min=fixture["expected_min"],
            expected_max=fixture["expected_max"],
            actual_score=actual_score,
            passed=passed,
            deviation=deviation
        )
        results.append(result)
        
        if verbose:
            status = "✅ PASS" if passed else f"❌ FAIL (off by {deviation} points)"
            print(f"Actual:   {actual_score}/100  →  {status}")
    
    all_passed = all(r.passed for r in results)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Calibration: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        
        if not all_passed:
            failed = [r for r in results if not r.passed]
            print(f"\n⚠️  {len(failed)} fixture(s) out of range:")
            for r in failed:
                if r.actual_score > r.expected_max:
                    print(f"   {r.fixture_id}: Overscoring by {r.deviation} points → Evaluator too lenient")
                else:
                    print(f"   {r.fixture_id}: Underscoring by {r.deviation} points → Evaluator too harsh")
            
            print("\n📋 Calibration Advice:")
            overscoring = sum(1 for r in failed if r.actual_score > r.expected_max)
            underscoring = sum(1 for r in failed if r.actual_score < r.expected_min)
            
            if overscoring > underscoring:
                print("   → Evaluator is systematically too lenient (grade inflation)")
                print("   → Add to Evaluator prompt: 'Do NOT award > 85 unless all critical")
                print("     acceptance criteria are verifiably met via actual interaction'")
                print("   → Add calibration examples to few-shot section in evaluator prompt")
            else:
                print("   → Evaluator is systematically too harsh")
                print("   → Add to Evaluator prompt: 'Do NOT award < 40 unless the primary")
                print("     user task is completely broken or inaccessible'")
    
    return all_passed, results


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("DoubleAgent Evaluator Calibration")
    print("="*60)
    print("To use this script, implement the evaluator_fn parameter in run_calibration().")
    print("This function should call your actual Evaluator agent and return a score (0-100).")
    print()
    print("Example implementation:")
    print()
    print("  def my_evaluator(description: str) -> int:")
    print("      # Call your evaluator agent here")
    print("      # Return integer score 0-100")
    print("      pass")
    print()
    print("  calibrated, results = run_calibration(my_evaluator)")
    print()
    print("See references/evaluator-prompts.md for Evaluator prompt templates.")
    sys.exit(0)
