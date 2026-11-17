## Description:

Scans installed skills, suggests L0-L3 priority tiers, and auto-configures skill injection policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to audit installed skills, assign L0-L3 priority tiers, and generate policy and setup guidance for token-budgeted skill injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can write persistent OpenClaw policy files and backups under the user's OpenClaw workspace.

Mitigation: Run with --dry-run first, review the proposed tier assignments, and inspect generated files before applying changes.

Risk: The script reports that AGENTS.md, SOUL.md, or message injector configuration were updated even when those changes are not actually implemented.

Mitigation: Verify those files manually after execution and do not rely on success messages alone.

Risk: Automatic mode may classify oddly named or untrusted skill directories using simple name-pattern rules.

Mitigation: Use the interactive review flow for mixed or untrusted skill collections and avoid --auto until the discovered skills are known.

## Reference(s):

- [Skill Priority Setup on ClawHub](https://clawhub.ai/halfmoon82/skills/skill-priority-setup)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance, terminal output, and generated local policy files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent OpenClaw policy files and backups when run outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
