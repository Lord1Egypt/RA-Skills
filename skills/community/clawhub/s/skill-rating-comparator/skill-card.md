## Description:

Automatically compares similar skills across functionality, code quality, documentation, user reviews, update frequency, and installation ease, then generates a scored report with recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill evaluators use this skill to compare a target ClawHub skill against similar skills before choosing, recommending, or improving a skill. It is intended to produce an advisory comparison report across six scoring dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected release presents mock and random ratings as if they came from real skill and repository analysis.

Mitigation: Treat generated rankings and recommendations as advisory, and verify skill metrics against authoritative ClawHub or repository sources before making selection decisions.

Risk: Users may mistake generated comparison reports for deterministic factual evaluations.

Mitigation: Review report outputs before sharing or relying on them, especially when comparing third-party skills or making procurement-style decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/skill-rating-comparator)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with score tables, dimension details, strengths, weaknesses, recommendations, and radar chart data as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores and rankings should be treated as advisory because the inspected release uses mock and random rating data.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, skill.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
