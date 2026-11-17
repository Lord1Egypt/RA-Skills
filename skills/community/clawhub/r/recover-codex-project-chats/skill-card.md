## Description:

Helps recover missing local Codex or ChatGPT Desktop projects, chats, and sidebar spaces after account or workspace changes, and diagnose lost assignments, provider mismatches, archived or invisible histories, moved paths, and backup compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Codex and ChatGPT Desktop users use this skill to diagnose missing project chats, review recovery evidence, and perform guarded local repairs while preserving backups and account boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that backups may include credentials or cloud state despite the stated exclusion.

Mitigation: Review backup scope and contents, and keep recovery backups local.

Risk: The security review reports that the installer uses an unpinned package.

Mitigation: Review the installer and dependency version before running it.

## Reference(s):

- [Account-switch recovery guide](references/account-switch-recovery.md)
- [Codex project-chat recovery patterns](references/incident-patterns.md)
- [ClawHub release page](https://clawhub.ai/songhonglei/skills/recover-codex-project-chats)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell commands and recovery steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnosis findings and recovery reports; local changes require an explicit, reviewed repair step.]

## Skill Version(s):

1.1.0 (source: CHANGELOG.md and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
