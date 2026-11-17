## Description:

OpenClaw repair toolkit - automated diagnostics, backup/restore, and guided AI-assisted recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose startup, gateway, configuration, network, and skill-loading problems, then run guided repair, backup, restore, or reset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair, restore, and reset actions can change local OpenClaw state and overwrite or delete sessions.

Mitigation: Review the selected action and backup path before execution, require explicit confirmation for restore/reset steps, and keep a rollback backup outside the working OpenClaw directories.

Risk: Backup behavior can copy a GitHub token into local backups in plaintext.

Mitigation: Exclude secrets from backups by default or encrypt backup archives and scrub token files before sharing or storing them.

Risk: Installer paths can fetch and execute software from live external sources.

Mitigation: Prefer pinned package-manager installs or verified downloads, and remove curl-to-shell install paths before production use.

Risk: Firewall-disable guidance can weaken host network protections.

Mitigation: Use scoped connectivity diagnostics and firewall rules instead of disabling the firewall.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/solcal-recovery)
- [Publisher Profile](https://clawhub.ai/user/amrree)
- [Ollama Install](https://ollama.ai/install)
- [Homebrew](https://brew.sh)
- [Minimax API Endpoint](https://api.minimax.io)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local shell scripts that inspect or modify OpenClaw configuration, sessions, skills, logs, gateway state, backups, and optional Ollama setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
