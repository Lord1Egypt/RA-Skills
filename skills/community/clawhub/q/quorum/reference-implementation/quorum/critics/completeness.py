# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Completeness Critic — Coverage gaps, missing requirements, unaddressed edge cases.

Checks:
- Requirements in the rubric that the artifact does not address
- Sections that are mentioned but empty or skeletal
- Edge cases that should be handled but are not discussed
- Missing error handling, failure modes, or alternatives
- Promised content that is absent

Evidence requirement: Must cite both the gap (what's missing) and where
it's required (rubric criterion or implied by another part of the artifact).
"""

from __future__ import annotations

from quorum.critics.base import BaseCritic
from quorum.models import Rubric


class CompletenessCritic(BaseCritic):
    """
    Evaluates coverage gaps, missing requirements, and unaddressed edge cases.

    Completeness is about what's *not* there. Evidence must reference:
    - The rubric criterion that requires this content, OR
    - Another part of the artifact that implies this content is needed
    """

    name = "completeness"

    @property
    def system_prompt(self) -> str:
        return """You are the Completeness Critic for Quorum, a rigorous quality validation system.

Your role: Evaluate artifacts for coverage gaps, missing requirements, and unaddressed edge cases.

Your specific focus areas:
1. **Required sections missing** — Does the rubric require content that the artifact doesn't provide?
2. **Shallow treatment** — Topics that are mentioned but not meaningfully addressed (stub sections, "TBD", etc.)
3. **Edge cases** — Scenarios the artifact should address but doesn't (error conditions, boundary cases, failure modes)
4. **Broken promises** — Content that other parts of the artifact imply exists but doesn't (referenced sections that are empty, etc.)
5. **Requirement gaps** — Explicit rubric criteria that the artifact fails to satisfy

Critical rule: EVERY finding must include evidence — either:
- A direct quote showing the gap exists (e.g., an empty section, a stub)
- A rubric criterion ID that requires missing content
- A quote from the artifact that implies required content is missing

Do not flag things as "missing" without grounding. If you can't point to where it should be, don't flag it.
Be specific: "Section 3 mentions error handling will be covered in Appendix B, but Appendix B does not exist" is good.
"Error handling is missing" without grounding is not acceptable."""

    def build_prompt(self, artifact_text: str, rubric: Rubric) -> str:
        # Build a checklist from all rubric criteria — completeness evaluates ALL of them
        criteria_text = "\n".join(
            f"- [{c.id}] {c.criterion}\n"
            f"  Severity if missing: {c.severity.value}\n"
            f"  Evidence required: {c.evidence_required}\n"
            f"  Why it matters: {c.why}"
            for c in rubric.criteria
        )

        return f"""## Artifact Under Review

```
{artifact_text}
```

## Rubric: {rubric.name} (v{rubric.version})

Domain: {rubric.domain}
{f"Description: {rubric.description}" if rubric.description else ""}

### All Criteria to Check for Completeness
{criteria_text}

## Your Task

For each rubric criterion above, determine: does the artifact adequately address it?

For any criterion NOT adequately addressed:
1. Quote the relevant (absent or skeletal) section of the artifact
2. Reference the rubric criterion ID that requires this content
3. Explain specifically what is missing or underdeveloped
4. Rate severity: CRITICAL (core requirement absent), HIGH (important gap), MEDIUM (notable), LOW (minor)

If a criterion IS adequately addressed, do not report it — only report gaps.

Also flag any edge cases, failure modes, or boundary conditions that the artifact's own framing implies should be addressed but aren't.

Return an empty findings list if the artifact is complete."""
