## Description:

Skill Discoverer helps OpenClaw agents discover newly published skills, recommend relevant additions, assess installation risk, and create scheduled skill-scan digests after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr23334444](https://clawhub.ai/user/dr23334444)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor the skill marketplace, find skills that match their current work, evaluate installation impact, and schedule recurring discovery reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads profile and recent-memory context to personalize skill recommendations.

Mitigation: Install only when that context access is acceptable for the workspace and review recommendation reports before acting on them.

Risk: The skill stores chat routing identifiers and can create recurring scan jobs.

Mitigation: Confirm the saved channel configuration and scheduled scan cadence before enabling recurring reports.

Risk: Learning and transformation mode can propose persistent changes to core agent behavior files.

Mitigation: Inspect each proposed rule and destination file individually, and decline self-preference or behavior-changing rules unless they are intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dr23334444/skills/skill-discoverer)
- [Search command guidance](references/search-commands.md)
- [Installation decision rules](references/install-decision.md)
- [ClawHub fallback safety rules](references/clawhhub-safety.md)
- [Learning and transformation workflow](references/step6b-learn-transform.md)
- [Example conversations](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before installation, learning, or persistent scheduling actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, changelog released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
