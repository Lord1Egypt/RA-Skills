## Description:

Universal smart routing skill that chooses the best installed skill or skill chain across mixed environments, and automatically applies OpenClaw-aware routing when an OpenClaw workspace or skill inventory is detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to choose the best installed skill or short skill chain for a request when capabilities overlap, constraints are unclear, or an OpenClaw-aware workflow may be available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked implicitly and inspect visible skill metadata or environment indicators before recommending a route.

Mitigation: Review the routing decision before acting on it, and use explicit skill selection for sensitive workflows.

Risk: Incomplete or stale installed-skill metadata can lead to a low-confidence or unsuitable recommendation.

Mitigation: Keep skill metadata current and follow the skill's fallback behavior by asking clarifying questions when confidence is weak.

## Reference(s):

- [Smart Router Omni on ClawHub](https://clawhub.ai/e2e5g/skills/smart-router-omni)
- [Scoring Rubric](references/scoring-rubric.md)
- [Ambiguity And Fallbacks](references/ambiguity-and-fallbacks.md)
- [Environment Detection](references/environment-detection.md)
- [Chain Patterns](references/chain-patterns.md)
- [Research Notes 2026-03](references/research-notes-2026-03.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown routing decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mode, recommendation, confidence, prerequisites, fallbacks, suggested chain, and clarification questions when needed.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
