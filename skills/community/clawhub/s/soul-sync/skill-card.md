## Description:

Personalizes an OpenClaw agent through adaptive conversation, optional account and data imports, and generated SOUL.md, USER.md, and MEMORY.md profile files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocbenji](https://clawhub.ai/user/ocbenji)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to bootstrap or refine personal agent profiles without a long setup process. It helps an agent collect user preferences, optionally analyze approved personal data sources, and prepare profile files for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can derive sensitive personal profiles from account, social, contact, YouTube, and local-system sources.

Mitigation: Use optional imports only after explicit consent, skip sources that are not needed, and review generated SOUL.md, USER.md, and MEMORY.md content before writing it.

Risk: OAuth credentials or API tokens could remain in a synced or committed workspace.

Mitigation: Keep credentials out of version control and synced folders, and remove unused tokens or credential files after testing.

Risk: Temporary profile artifacts may remain after testing.

Mitigation: Delete /tmp/soulsync and .soulsync-state.json when retained profile data is no longer wanted.

## Reference(s):

- [Soul Sync ClawHub Page](https://clawhub.ai/ocbenji/skills/soul-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON status, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SOUL.md, USER.md, and MEMORY.md profile content after user review; optional importers may create temporary JSON insight files.]

## Skill Version(s):

0.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
