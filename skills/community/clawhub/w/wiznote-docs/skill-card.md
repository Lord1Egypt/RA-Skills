## Description:

Use when documents must be read from or maintained in a WizNote or 为知笔记 server, mirrored into a local repository, or organized under a configurable note category root.

This skill is ready for commercial/non-commercial use.

## Publisher:

[735140144](https://clawhub.ai/user/735140144)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and small teams use this skill to connect an agent workflow to a user-supplied WizNote server, read or maintain notes, and mirror selected documentation into a local repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WizNote passwords, tokens, and note content without enough transport and endpoint safeguards.

Mitigation: Use only a trusted WizNote server over HTTPS, avoid plaintext HTTP, and add same-origin or allowlist checks for kbServer before using sensitive notes.

Risk: Create and save helpers perform real remote writes to the configured WizNote server.

Mitigation: Require explicit confirmation before write operations, list existing notes before changes, and re-list the category afterward to verify the result.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [README.zh-CN](artifact/README.zh-CN.md)
- [ClawHub Skill Page](https://clawhub.ai/735140144/skills/wiznote-docs)
- [ClawHub Publisher Profile](https://clawhub.ai/user/735140144)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; helper calls may also create or update remote WizNote notes and local mirror files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied WizNote base URL, credentials, category root, and repository root; create and save helpers perform remote writes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
