## Description:

SenseNova Team Harness helps users understand and get started with a self-hosted workspace where people and local AI agents collaborate on conversations, projects, work items, and artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, team leads, and operators use this skill to understand SenseNova Team Harness, decide whether it fits their work, and follow the self-hosted setup and basic collaboration workflow for human-agent projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-hosted service is described as an early project and not a production security boundary.

Mitigation: Keep deployments private until identity, TLS, backups, monitoring, rate limits, and threat modeling are added.

Risk: Local configuration, credentials, databases, work directories, and logs may contain sensitive data.

Mitigation: Do not commit .env files, tokens, SQLite databases, local work directories, or logs to source control.

Risk: Installation depends on source checkout and npm dependencies.

Mitigation: Verify the repository and dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-team-harness)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup and usage guidance; it does not execute code by itself.]

## Skill Version(s):

2026.9.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
