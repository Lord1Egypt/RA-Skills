# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Correctness Critic — Factual accuracy, logical consistency, internal contradictions.

Checks:
- Claims that are internally contradicted within the artifact
- Logical inconsistencies and non-sequiturs
- Missing or false citations/references
- Stated facts that conflict with each other
- Faulty reasoning chains

Evidence requirement: Must quote the specific text that is incorrect or contradicted.
"""

from __future__ import annotations

from quorum.critics.base import BaseCritic
from quorum.models import Rubric


class CorrectnessCritic(BaseCritic):
    """
    Evaluates factual accuracy, logical consistency, and internal contradictions.

    Uses Tier 2 model by default (overridable). Evidence must be direct quotes
    or specific references from the artifact.
    """

    name = "correctness"

    @property
    def system_prompt(self) -> str:
        return """You are the Correctness Critic for Quorum, a rigorous quality validation system.

Your role: Evaluate artifacts for factual accuracy, logical consistency, and internal contradictions.

Your specific focus areas:
1. **Internal contradictions** — Does the artifact contradict itself? Are statements in one section incompatible with another?
2. **Logical consistency** — Do the conclusions follow from the premises? Are there non-sequiturs or unsupported leaps?
3. **Factual claims** — Are stated facts plausible and internally coherent? Flag claims that appear unsubstantiated.
4. **Reference accuracy** — Are citations, names, and quoted figures internally consistent?
5. **Terminology consistency** — Is the same concept described by conflicting terms in different sections?

Critical rule: EVERY finding must include a direct quote or specific excerpt from the artifact as evidence.
If you cannot quote the artifact to support a finding, do not report it.
Vague claims like "this section is unclear" without evidence will be rejected.

Be precise, be fair, be thorough. Do not invent issues. Do not hallucinate quotes."""

    def build_prompt(self, artifact_text: str, rubric: Rubric) -> str:
        # Extract correctness-relevant criteria from the rubric
        relevant_criteria = [
            c for c in rubric.criteria
            if any(
                kw in c.criterion.lower()
                for kw in [
                    "accurate", "correct", "consistent", "factual", "logical",
                    "contradict", "valid", "truth", "claim", "support",
                ]
            )
        ] or rubric.criteria  # Fall back to all criteria if none match

        criteria_text = "\n".join(
            f"- [{c.id}] {c.criterion} (Severity: {c.severity.value})\n"
            f"  Evidence required: {c.evidence_required}"
            for c in relevant_criteria
        )

        return f"""## Artifact Under Review

```
{artifact_text}
```

## Rubric: {rubric.name} (v{rubric.version})

Domain: {rubric.domain}

### Criteria to Evaluate
{criteria_text}

## Your Task

Review the artifact above for correctness issues. For each finding:
1. Quote the specific text from the artifact that is problematic
2. Explain the correctness violation clearly
3. Identify which rubric criterion it violates (if any)
4. Assign a severity: CRITICAL (fatal flaw), HIGH (significant), MEDIUM (notable), LOW (minor), INFO (FYI)

If the artifact is entirely correct, return an empty findings list.
Only report findings you can back up with direct quotes from the artifact."""
