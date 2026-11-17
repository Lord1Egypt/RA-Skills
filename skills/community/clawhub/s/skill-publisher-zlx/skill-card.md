## Description:

Publishes Agent skills to ClawHub, GitHub Releases, and SkillHub CN with validation, packaging, version management, and multi-platform release commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlx](https://clawhub.ai/user/zlx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate, package, version, inspect status, and publish local OpenClaw Agent skills to multiple release platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing an unreviewed skill directory could leak unintended files.

Mitigation: Audit the exact directory and generated archive before publishing, and keep secrets, .env files, private keys, backups, and repository metadata out of the skill folder.

Risk: Version or publish commands on an untrusted skill directory could run unsafe behavior.

Mitigation: Run these commands only on trusted, reviewed skill directories and avoid --yes until the archive contents and target platforms have been checked.

## Reference(s):

- [Skill Publisher on ClawHub](https://clawhub.ai/zlx/skills/skill-publisher-zlx)
- [Adding Platform Adapters](artifact/references/adding-platforms.md)
- [Platform Interface Specification](artifact/references/platform-interface.md)
- [SkillHub CN](https://skillhub.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local tarballs, update SKILL.md versions, call external platform CLIs, and write publish history without credentials.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
