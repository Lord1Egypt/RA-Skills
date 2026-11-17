## Description:

Automatically detects, backs up, and updates installed OpenClaw skills with caching, retry logic, dry-run previews, and upgrade reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thunder1743](https://clawhub.ai/user/thunder1743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local OpenClaw skill installations, preview available updates, apply selected upgrades, and preserve backups for rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically replace installed local skills with downloaded packages that are not independently verified.

Mitigation: Use dry-run first, avoid automatic updates for untrusted or important environments, and install only when the publisher is trusted.

Risk: An update may break an existing local skill or introduce unwanted behavior.

Mitigation: Review the backup under ~/Desktop/skill-backups/ before and after updating, and restore from the backup if the update is not acceptable.

Risk: HTTPS transport alone does not prove a downloaded package is the intended publisher's signed release.

Mitigation: Treat registry downloads as unsigned unless separate provenance or signature evidence is provided.

## Reference(s):

- [ClawHub Skills Updater listing](https://clawhub.ai/thunder1743/skills/skills-updater)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text, shell commands, and Markdown upgrade reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timestamped backups and an upgrade report when updates are performed.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
