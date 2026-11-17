## Description:

Windows Dev Pitfalls is a reference skill for diagnosing and avoiding Windows batch, PowerShell, Win32 GUI, Flutter desktop, encoding, elevation, sandbox-testing, and delivery pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill as a troubleshooting vault for Windows scripting, desktop GUI, Flutter desktop adaptation, and delivery review. It helps identify recurring failure modes such as encoding damage, cmd syntax traps, UAC/elevation issues, Wine validation gaps, and risky remediation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a mutable living reference and asks agents to persistently update the skill content.

Mitigation: Require explicit user approval before editing the skill, review diffs before preserving new guidance, and keep version and changelog updates tied to approved changes.

Risk: The reference includes high-impact remediation examples involving hosts files, firewall rules, services, permissions, watchdog behavior, and delete or quarantine flows.

Mitigation: Treat these examples as advisory; require explicit confirmation, backups, and a rollback or dry-run path before applying system-changing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mowenqwq/skills/win-dev-pitfalls)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes troubleshooting checklists and command snippets; no agent-executable tool interface is defined.]

## Skill Version(s):

1.71.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
