## Description:

Ranks skill ideas by frequency, entry barrier, virality, ROI, and risk to produce a structured prioritization brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and release planners use this skill to compare candidate skill topics, identify high-potential and low-priority ideas, and turn incomplete input into a reviewable roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prioritization output may be mistaken for an objective quantitative ranking engine.

Mitigation: Treat the result as a review draft and validate scoring assumptions, market facts, and release priorities before acting on it.

Risk: Input materials may contain sensitive skill plans, customer details, or publisher strategy.

Mitigation: Redact sensitive content before use and keep generated briefs within the intended review workflow.

Risk: The packaged helper includes broader audit logic even though the configured workflow is non-destructive.

Mitigation: Run it on trusted local inputs, review generated commands before use, and keep the workflow in draft or dry-run mode for high-risk changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-market-fit-ranker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown brief, with optional JSON output from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input materials and highlights missing information instead of filling gaps with unsupported assumptions.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
