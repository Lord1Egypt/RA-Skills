## Description:

Manage agent memory with Membase - a decentralized, encrypted memory backup and restore system. Provides backup, restore, list, diff, status, and cleanup operations for agent memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibitnoah](https://clawhub.ai/user/ibitnoah)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to back up, restore, list, compare, and inspect OpenClaw agent memory files with Membase-backed encrypted storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal workflows can expose credentials or backup passwords through echoed environment variables, command-line password arguments, or status JSON.

Mitigation: Do not use real credentials or backup passwords until secret checks use non-disclosing presence checks, password arguments are avoided, and status JSON is redacted.

Risk: Restore operations can write memory files back into the configured workspace without clear staging or overwrite confirmation.

Mitigation: Review restore behavior before use and require staging or explicit overwrite confirmation for restored files.

Risk: The reviewed artifact imports implementation modules from an unbundled lib path.

Mitigation: Install only a reviewed package that includes the actual lib implementation rather than relying on an external symlink.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ibitnoah/skills/unibase-membase)
- [Membase Documentation](https://github.com/unibaseio/membase)
- [AgentSkills Specification](https://agentskills.io)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may emit machine-readable JSON between JSON_OUTPUT markers for agent parsing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
