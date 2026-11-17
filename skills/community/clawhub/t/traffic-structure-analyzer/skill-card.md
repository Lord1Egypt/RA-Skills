## Description:

Analyze traffic composition and quality trends from Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

External users and advertising analysts use this skill to decompose paid traffic mix, diagnose traffic quality trends, compare campaign metrics, and turn channel-specific findings into actionable recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad business-performance questions that are not specifically advertising traffic analysis.

Mitigation: Clarify whether the user wants advertising traffic analysis before applying channel-specific campaign guidance.

Risk: Recommendations can be misleading when metric definitions, attribution windows, date ranges, or data-source scope are missing or inconsistent.

Mitigation: Lock canonical metric definitions, time windows, and data sources before analysis; label low-confidence conclusions as directional and include validation steps.

Risk: Budget or campaign recommendations may create spend risk if treated as final decisions without review.

Mitigation: Use measurable next actions with rollback or stop-loss conditions, and escalate policy, billing, or tracking issues with a structured handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/traffic-structure-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown with structured advertising analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces metric clarification, query plans, result summaries, interpretation caveats, and decision recommendations; no executable code is included.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
