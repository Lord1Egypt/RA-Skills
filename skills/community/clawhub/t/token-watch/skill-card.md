## Description:

Token Watch helps agents and developers track AI API token usage, estimate costs, set budget alerts, compare model prices, and export local usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vedantsingh60](https://clawhub.ai/user/vedantsingh60)

### License/Terms of Use:

MIT

## Use Case:

Developers, AI power users, and agents use Token Watch to monitor token spending across AI providers, compare model costs before calls, configure budgets, and review locally stored usage history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local usage history and exported reports can include model names, token counts, costs, timestamps, task labels, and session IDs.

Mitigation: Use generic task labels for sensitive work, review exported reports before sharing, and delete or relocate the .tokenwatch storage directory when local retention is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vedantsingh60/skills/token-watch)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores usage, budget, and alert history locally in .tokenwatch by default.]

## Skill Version(s):

1.2.3 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
