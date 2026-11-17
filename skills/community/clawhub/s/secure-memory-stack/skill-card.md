## Description:

A secure local memory system combining Baidu Embedding semantic search, Git Notes structured storage, and filesystem-backed memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqicxx](https://clawhub.ai/user/xqicxx)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to initialize, configure, search, and maintain a local memory stack that combines semantic search, Git Notes, and Markdown file storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy and offline-use claims may not hold when Baidu Embedding is enabled.

Mitigation: Do not rely on zero-upload claims until data flows are documented; avoid storing secrets or regulated data when external embedding APIs are configured.

Risk: Permission repair, cleanup, verification, and refresh paths operate broadly in a shared /root/clawd workspace.

Mitigation: Audit scripts before execution and run them only in an isolated or clearly scoped workspace.

Risk: The security verdict is suspicious and the scanner summary says the skill is too broad or unsafe for automatic trust.

Mitigation: Review and scan the skill before installation or deployment, and require human approval before running maintenance or repair commands.

## Reference(s):

- [Secure Memory Stack README](artifact/README.md)
- [Secure Memory Stack Documentation](artifact/DOCUMENTATION.md)
- [Installation Guide](artifact/INSTALLATION.md)
- [Memory System Guide](artifact/MEMORY_SYSTEM_GUIDE.md)
- [Baidu AI Cloud](https://cloud.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local configuration or memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local memory, session, notes, and configuration files under the configured /root/clawd workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG released 2026-01-31, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
