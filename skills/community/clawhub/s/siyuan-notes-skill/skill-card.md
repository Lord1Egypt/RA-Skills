## Description:

SiYuan note-management skill for searching, reading, editing, organizing, and querying notes through a Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanxing-6](https://clawhub.ai/user/fanxing-6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate against a SiYuan knowledge base: searching, reading, editing, organizing, querying, and creating notes while following the skill's read-before-write workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or sensitive SiYuan workspaces may expose private notes or credentials if configured over insecure transport.

Mitigation: Use HTTPS for any non-localhost SiYuan host, keep tokens out of URLs, and review the skill before connecting it to sensitive notes.

Risk: Write-capable commands can modify or delete notes when write mode is enabled.

Mitigation: Leave write mode disabled by default and enable it only for intentional edits after reading the target document or section.

Risk: Mutable main-branch installation can change the code installed for future runs.

Mitigation: Prefer a pinned release artifact instead of the mutable main-branch install command.

Risk: Broad shell authority increases review burden before installation.

Mitigation: Review the skill behavior and security summary before installing, especially for remote or sensitive SiYuan servers.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fanxing-6/skills/siyuan-notes-skill)
- [SiYuan](https://b3log.org/siyuan/)
- [Claude Code](https://claude.com/claude-code)
- [Command Reference](docs/command-reference.md)
- [PMF Specification](docs/pmf-spec.md)
- [SQL Reference](docs/sql-reference.md)
- [Error Recovery](docs/Error-Recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and concise command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations may return formatted text or Markdown; write operations should surface concise success or failure details.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
