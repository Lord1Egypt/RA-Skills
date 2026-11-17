## Description:

YoudaoNote lets agents use the youdaonote CLI to create, read, update, delete, search, clip, and organize notes and todos in a connected YoudaoNote account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lephix](https://clawhub.ai/user/lephix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent manage YoudaoNote content through the youdaonote CLI, including notes, folders, web clips, search, and todos. It is intended for normal connected-account workflows rather than knowledge-base or Wiki generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run an unpinned remote shell installer.

Mitigation: Download and inspect the installer before execution, and prefer a version-pinned or checksum-verified installation method when available.

Risk: The skill can change or delete notes, folders, web clips, and todos in the connected YoudaoNote account.

Mitigation: Review proposed write, move, and delete operations before execution, especially when account content is sensitive or difficult to recover.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lephix/skills/youdaonote)
- [YoudaoNote Homepage](https://note.youdao.com)
- [YoudaoNote CLI Install Guide](https://note.youdao.com/help-center/cli-install-guide.html)
- [YoudaoNote API Key Portal](https://mopen.163.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through the youdaonote CLI and may read, create, update, move, or delete content in the connected account.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
