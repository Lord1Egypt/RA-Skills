## Description:

Saves markdown content to remote Obsidian vault via SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to save agent-generated Markdown notes to a remote Obsidian vault over SSH while applying Obsidian-friendly formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SSH upload script can transfer arbitrary readable files to runtime-supplied destinations.

Mitigation: Use a dedicated SSH key restricted to the intended vault, keep the vault destination fixed in trusted configuration, upload only staged Markdown files, and require confirmation before transfer or overwrite.

Risk: A broad agent file-access context could expose sensitive local files if an unintended source path is uploaded.

Mitigation: Limit source paths to temporary agent-created Markdown files and review the source file before invoking scp.

Risk: Duplicate filenames may overwrite existing vault notes silently.

Mitigation: Confirm overwrite intent or generate unique filenames before transfer.

## Reference(s):

- [Obsidian Markdown Guide](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Obsidian Mermaid Support](https://help.obsidian.md/Editing+and+formatting/Advanced+formatting+syntax#Diagram)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes with shell command invocations and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transfers staged Markdown files with sanitized filenames to a configured remote vault via scp.]

## Skill Version(s):

1.1.0 (source: skill.yml, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
