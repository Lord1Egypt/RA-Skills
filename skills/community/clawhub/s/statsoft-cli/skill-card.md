## Description:

Connects AI agents to locally installed statistical software to detect tools, configure integrations, and run existing analysis scripts across supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to discover local statistical tools, connect existing projects to agent workflows, and run supported statistical scripts or data conversions with user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted filenames in untrusted directories may cause the Windows launcher to execute unintended shell commands.

Mitigation: Review or patch the Windows launcher before running execution wrappers, especially batch conversion; inspect input filenames and prefer structured process arguments over cmd.exe command strings.

Risk: Broadly enabling automatic writes or confirmation can authorize scans or configuration changes beyond the intended task.

Mitigation: Keep STATSOFT_AUTO_WRITE and STATSOFT_CONFIRM unset by default; inspect planned commands and grant approval for the specific operation.

Risk: Running local statistical software or user scripts may execute untrusted code or alter project files.

Mitigation: Review scripts and generated commands before execution and use trusted inputs and software installations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/medstatstar/skills/statsoft-cli)
- [Project homepage and documentation](https://github.com/medstatstar/statsoft-cli)
- [Platform support](references/platform-support.md)
- [Trust and safety](references/trust-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and setup summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report detected software and paths when authorized; configuration changes require opt-in.]

## Skill Version(s):

2.8.4 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
