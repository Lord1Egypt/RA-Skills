## Description:

Manage Turso SQLite databases via CLI - databases, groups, tokens, replicas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Turso and libSQL databases from an agent workflow, including database, group, organization, plan, and token operations through the Turso CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux setup path runs a mutable remote shell installer.

Mitigation: Review or replace the installer with an official package or verified download before installation.

Risk: The skill includes destructive database and group commands, plan upgrades, organization switching, and token commands.

Mitigation: Require explicit user confirmation before destroy, upgrade, organization switch, token display, or non-expiring token creation commands.

Risk: Auth tokens may expose access to Turso resources.

Mitigation: Treat tokens as secrets and prefer short-lived, least-privilege credentials.

## Reference(s):

- [ClawHub Turso skill page](https://clawhub.ai/melvynx/skills/turso)
- [Turso Linux installer](https://get.tur.so/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for programmatic Turso CLI access where supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
