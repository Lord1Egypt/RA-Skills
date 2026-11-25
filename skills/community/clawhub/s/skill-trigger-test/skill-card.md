## Description:

Evaluates whether agent skills trigger for intended user messages and stay silent for neighboring intents, then summarizes results in a scorecard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Developers maintaining agent skills can assess trigger misses, false alarms, and overlaps by testing generated or supplied user messages and reviewing a scorecard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security report flags a privacy concern about reusing real user messages in reusable skill metadata; the scan was partial.

Mitigation: Prefer synthetic test messages, and redact sensitive details from real messages before using them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/thomaszhou22/skills/skill-trigger-test)
- [Analysis Protocol](references/analysis-protocol.md)
- [Trigger Test Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown scorecard with per-skill tables and failure details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No model or external API calls; test messages may be generated, user-supplied, or both.]

## Skill Version(s):

1.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
