## Description:

CLI tool to manage SSH config files, organize hosts, generate configs, and test connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect, organize, validate, back up, and update SSH client configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify SSH client configuration, which may disrupt access or change connection behavior if entries are malformed or unintended.

Mitigation: Review proposed changes before applying them and keep an independent backup of ~/.ssh/config.

Risk: Connection testing can initiate SSH attempts to hosts named in configuration files.

Mitigation: Avoid testing hosts from untrusted config files and verify target hosts before running test commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derick001/skills/ssh-config-manager)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, write, validate, back up, and test SSH client configuration depending on the selected command.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
