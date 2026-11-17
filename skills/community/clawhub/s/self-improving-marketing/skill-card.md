## Description:

Records marketing performance issues and learnings in local Markdown logs so teams can improve campaigns, messaging, and attribution over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and their agents use this skill to capture campaign setbacks, messaging misses, audience changes, and attribution gaps, then review recurring lessons for incorporation into marketing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning logs may contain customer personal data, credentials, transcripts, or sensitive revenue figures.

Mitigation: Exclude sensitive details from logs and review entries before sharing or committing them.

Risk: Optional hooks may add reminders or inspect tool output beyond the intended marketing workflow.

Mitigation: Keep hooks project-scoped, use narrow marketing matchers, and leave PostToolUse disabled unless output scanning is intended.

Risk: Promoted guidance or extracted skills may carry inaccurate or unreviewed marketing claims.

Mitigation: Review proposed changes and generated skills before adopting or publishing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jose-compu/skills/self-improving-marketing)
- [Hook setup guidance](artifact/references/hooks-setup.md)
- [OpenClaw integration guidance](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Text guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown learning and issue entries with optional setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project-local learning logs; can suggest reviewed updates to marketing guidance or a reusable skill.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
