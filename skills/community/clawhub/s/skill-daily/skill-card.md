## Description:

Clawhub Daily scans ClawHub skills, ranks them across recommendation dimensions, and generates concise daily briefings with optional delivery to Feishu, IMA, Obsidian, and local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, team leads, content creators, and ClawHub users use this skill to monitor AI Agent Skill trends, avoid repeated recommendations, and receive a short daily briefing tailored to common workflow pain points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled network fetching and report pushes may transmit generated briefings to external services when credentials are configured.

Mitigation: Run with --skip-push or leave push credentials unset for local-only operation; review configured Feishu and IMA destinations before enabling scheduled delivery.

Risk: IMA delivery can use a built-in knowledge-base ID or fall back to a locally resolved CLI command in auto mode.

Mitigation: Set an explicit kb_id, prefer --mode official, and avoid auto CLI fallback unless the local ima-skill executable path is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/skill-daily)
- [Setup wizard](references/setup-wizard.md)
- [Prompt templates](references/prompt-templates.md)
- [API contract](references/api-contract.md)
- [Source data schema](references/source-data-schema.md)
- [Briefing template](references/briefing-template.md)
- [Pain points](references/pain-points.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings, JSON recommendation files, local files, and optional pushed reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates daily snapshots, metrics, recommendation outputs, and concise briefing content; external delivery depends on configured credentials and skip flags.]

## Skill Version(s):

2.0.8 (source: frontmatter, evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
