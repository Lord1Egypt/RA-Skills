## Description:

SkillMetricScraper tracks trending ClawHub skills from API snapshots and generates weekly intelligence reports and voice-ready video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ademczuk](https://clawhub.ai/user/ademczuk)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to collect ClawHub skill metrics, rank trending skills, and produce weekly Markdown reports, JSON data, and voice-ready briefing scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow can use Docker access to copy metrics data from a running container.

Mitigation: Run in a least-privileged environment and use --no-bridge unless container database copying is explicitly intended.

Risk: Optional community capture and public skill content can influence generated Markdown, JSON, and scripts.

Mitigation: Treat generated artifacts as untrusted drafts and review them before publishing or feeding them into downstream pipelines.

Risk: Optional X/Twitter capture and script generation can require external API keys.

Mitigation: Provide only the keys needed for the selected mode and use --skip-x when X/Twitter capture is not required.

Risk: Dependency installation may pull packages from the configured Python package index.

Mitigation: Inspect or pin dependencies before running pip install in shared or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ademczuk/skills/skillmetricscraper)
- [Publisher Profile](https://clawhub.ai/user/ademczuk)
- [ClawHub Skills API](https://clawhub.ai/api/v1/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown reports, plain-text video scripts, JSON data files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local SQLite metrics database and dated report artifacts.]

## Skill Version(s):

1.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
