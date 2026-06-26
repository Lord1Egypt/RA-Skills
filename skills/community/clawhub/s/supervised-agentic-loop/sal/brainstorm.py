"""Hypothesis generation for the evolution loop.

v0.1: Template-based (deterministic) — generates hypotheses from
past results and learnings patterns without LLM calls.

🟡 Dr. Neuron finding: Templates v0.1 are now concrete.
"""

from pathlib import Path
from typing import Optional


# v0.1 hypothesis templates — categorized by experiment area
TEMPLATES: dict[str, list[str]] = {
    "hyperparams": [
        "Increase learning rate by 2x",
        "Decrease learning rate by 2x",
        "Increase batch size by 2x",
        "Decrease batch size by 2x",
        "Add learning rate warmup (100 steps)",
        "Switch to cosine annealing schedule",
        "Increase weight decay to 0.1",
        "Decrease weight decay to 0.01",
    ],
    "optimizer": [
        "Switch optimizer from Adam to AdamW",
        "Switch optimizer from AdamW to SGD with momentum",
        "Enable gradient clipping at max_norm=1.0",
        "Increase gradient clipping threshold to 5.0",
    ],
    "architecture": [
        "Add dropout layer (p=0.1) after each linear layer",
        "Increase model hidden size by 50%",
        "Decrease model hidden size by 50%",
        "Add layer normalization before each attention block",
        "Switch activation function to GeLU",
        "Switch activation function to SiLU/Swish",
    ],
    "regularization": [
        "Add label smoothing (0.1)",
        "Enable gradient accumulation (2 steps)",
        "Add data augmentation/noise",
    ],
    "efficiency": [
        "Enable mixed precision training (fp16)",
        "Reduce sequence length by 25%",
        "Increase sequence length by 25%",
    ],
}


def generate_hypothesis(
    results_history: list[dict],
    learnings_patterns: Optional[dict] = None,
    target_file: Optional[str] = None,
) -> dict:
    """Generate next experiment hypothesis based on history.

    Strategy (v0.1 deterministic):
    1. Avoid repeating hypotheses that already failed (from history).
    2. Prioritize areas that have been successful (from learnings).
    3. Cycle through template categories round-robin.
    4. If all templates exhausted, combine two approaches.

    Args:
        results_history: List of dicts from results.tsv history.
        learnings_patterns: Output from LearningsLog.get_patterns().
        target_file: Path to the file being modified (for context).

    Returns:
        Dict with keys:
            - description: Human-readable hypothesis.
            - area: Category (hyperparams, optimizer, etc.).
            - risk: "low" | "medium" | "high".
            - expected_direction: "better" | "uncertain".
    """
    # Collect used hypotheses
    used = {entry.get("hypothesis", "").lower() for entry in results_history}
    used.discard("")
    used.discard("baseline")

    # Determine area priority from learnings
    area_priority = list(TEMPLATES.keys())
    if learnings_patterns:
        # Prioritize areas with past successes
        successful = learnings_patterns.get("successful_areas", {})
        if successful:
            # Sort areas: most successful first
            area_priority = sorted(
                area_priority,
                key=lambda a: successful.get(a, 0),
                reverse=True,
            )

        # Deprioritize areas that keep failing
        failed = learnings_patterns.get("failed_areas", {})
        failed_hypotheses = {
            h.lower() for h in learnings_patterns.get("failed_hypotheses", [])
        }
        used.update(failed_hypotheses)

    # Find first unused template
    for area in area_priority:
        for template in TEMPLATES[area]:
            if template.lower() not in used:
                return {
                    "description": template,
                    "area": area,
                    "risk": _assess_risk(area),
                    "expected_direction": "uncertain",
                }

    # All templates used — generate combinations
    iteration_num = len(results_history)
    area = area_priority[iteration_num % len(area_priority)]
    combo = f"Combine: revisit {area} with modified parameters (iteration {iteration_num})"

    return {
        "description": combo,
        "area": area,
        "risk": "medium",
        "expected_direction": "uncertain",
    }


def _assess_risk(area: str) -> str:
    """Assess risk level of a hypothesis area."""
    risk_map = {
        "hyperparams": "low",
        "optimizer": "medium",
        "architecture": "high",
        "regularization": "low",
        "efficiency": "medium",
    }
    return risk_map.get(area, "medium")


def format_hypothesis_prompt(
    hypothesis: dict,
    target_file: str,
    target_content: Optional[str] = None,
) -> str:
    """Format a hypothesis as a concrete task prompt for the agent.

    Args:
        hypothesis: Output from generate_hypothesis().
        target_file: The file the agent should modify.
        target_content: Current file content (optional).

    Returns:
        Prompt string for the agent.
    """
    prompt = f"""## EXPERIMENT TASK

**Hypothesis:** {hypothesis["description"]}
**Area:** {hypothesis["area"]}
**Risk Level:** {hypothesis["risk"]}

**Target File:** `{target_file}` — this is the ONLY file you may modify.

**Instructions:**
1. Read the current `{target_file}`
2. Apply the hypothesis: {hypothesis["description"]}
3. Make the minimum changes needed — do NOT refactor unrelated code
4. Ensure the code still runs without errors after your changes

**Constraints:**
- Modify ONLY `{target_file}`
- Do NOT change the evaluation/metric reporting code
- Keep changes minimal and reviewable
"""

    if target_content:
        prompt += f"""
**Current file content ({len(target_content)} chars):**
```python
{target_content[:3000]}
```
"""

    return prompt
