## Description:

Query, install, update, and edit AI agent skills on compatible Skill Hubs, with authenticated support for private skills and unauthenticated support for public discovery and installs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search compatible Skill Hubs, inspect versions, install or update skills, manage skill card metadata, and perform team-member administration where the target Hub supports it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install remote skill packages into directories that may be loaded by future agent sessions.

Mitigation: Install only from trusted Hubs and review downloaded skills before enabling them.

Risk: Hub tokens may grant access to private skills or administrative endpoints.

Mitigation: Use least-privilege tokens and avoid storing broad tokens in shell startup files.

Risk: Edit and team commands can change Hub metadata or membership.

Mitigation: Treat these as administrative actions that require explicit human approval and post-write verification.

Risk: Security evidence notes credential and path-handling weaknesses.

Mitigation: Run the skill's diagnostic checks and keep installs scoped to trusted, least-privilege skill directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-hub-query)
- [Skill Hub API Reference](references/api.md)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown summaries with inline shell commands and JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or modify skill files after explicit human approval; query and administrative commands may emit JSON for machine-readable workflows.]

## Skill Version(s):

1.4.0 (source: server release evidence, SKILL.md, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
