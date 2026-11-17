## Description:

ClaWHub skill synchronization and automatic updates for detecting, updating, syncing, and reporting local skill version status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to check local workspace skills, compare versions, synchronize them with ClaWHub, and produce a difference report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to the configured ClaWHub account and token file for synchronization.

Mitigation: Install only for accounts intended to update local skills, avoid direct token-file reads where possible, and use a protected account configuration.

Risk: Bulk synchronization and publishing can update or publish many local skills at once.

Mitigation: Require a dry run and explicit confirmation before sync or publish actions, and restrict synchronization to approved skill directories.

Risk: The artifact suggests a fixed CLI path and optional daily cron automation.

Mitigation: Use a protected, pinned CLI path and leave recurring cron execution disabled unless ongoing publishing is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-skill-sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include version comparison results, synchronization status, and recommended confirmation steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata; artifact body also mentions 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
