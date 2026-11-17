## Description:

Unified Memory V5 provides persistent agent memory management with hybrid BM25/vector/RRF search, atomic transactions, WAL-backed consistency, lifecycle management, and plugin support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mouxangithub](https://clawhub.ai/user/mouxangithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, search, deduplicate, export, sync, and restore long-term agent memories. It can also feed remembered context into prompt workflows through OpenClaw hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories, prompt recalls, and exports can contain private or sensitive information.

Mitigation: Treat memory stores and exports as sensitive data and restrict access, sharing, backup, and sync destinations to trusted systems.

Risk: Backup, restore, sync, delete, plugin, and cron-style automation can change or move memory data in broad ways.

Mitigation: Require explicit operator confirmation before export, delete, restore, plugin registration, backup, sync, or scheduled automation actions.

Risk: The artifact documentation includes a curl-to-shell installation path.

Mitigation: Do not use curl-to-shell installation; install only after reviewing the publisher and package contents.

Risk: Plugin hooks can modify stored memories or search behavior and may call external services.

Mitigation: Enable only trusted plugins and review plugin configuration before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mouxangithub/skills/unified-memory-v5)
- [Artifact README](artifact/README.md)
- [Artifact Installation Guide](artifact/INSTALL.md)
- [Artifact Technical Reference](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Shell commands]

**Output Format:** [MCP tool responses, Markdown documentation, JSON/CSV/Markdown exports, and command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs and exports may contain private stored memories and should be treated as sensitive.]

## Skill Version(s):

5.2.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
