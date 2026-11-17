## Description:

MCP server for SilverBullet note-taking app - read, write, search, and manage markdown pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramonitor](https://clawhub.ai/user/ramonitor)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect an MCP-compatible client to a SilverBullet note space for reading, writing, searching, and managing markdown pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete note data through write, append, and delete tools.

Mitigation: Use it only with a SilverBullet server you control, review write and delete operations before execution, and keep backups for important notes.

Risk: Per-call base_url values can redirect tool requests to arbitrary URLs.

Mitigation: Avoid letting prompts or untrusted content supply base_url values; prefer a version that removes or validates per-call URL overrides.

Risk: Dependencies are declared with broad minimum versions.

Mitigation: Pin dependencies before production deployment and review updates before installing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramonitor/skills/silverbullet-skill)
- [SilverBullet](https://silverbullet.md)
- [SilverBullet HTTP API](https://silverbullet.md/HTTP%20API)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown, JSON-like tool responses, and plain-text status or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and uv; tools operate against a configured SilverBullet server URL.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
