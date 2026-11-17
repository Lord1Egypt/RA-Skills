## Description:

XiaxiaBao Doc Manager helps agents organize Feishu documents across Wiki, Drive, and Bitable with automatic classification, archiving, search, backup, and template-based document creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uuoov](https://clawhub.ai/user/uuoov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to manage Feishu document lifecycles: creating documents, placing them in the right Wiki and Drive locations, maintaining Bitable indexes, finding documents, generating templates, and preparing backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup workflow can upload sensitive local memory and configuration files to Feishu.

Mitigation: Remove the default MEMORY.md and openclaw.json backup sources, redact sensitive content, and require explicit approval before any local file is uploaded.

Risk: Configured Feishu identifiers point to fixed Wiki, Drive, and Bitable destinations.

Mitigation: Use only Feishu resources controlled by the installer and replace all default identifiers during setup.

Risk: Backup cleanup can delete older backup copies automatically.

Mitigation: Require explicit approval before deleting backups and verify retention settings before enabling scheduled cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uuoov/skills/xiaxiabao-doc-manager)
- [Feishu Open Platform](https://open.feishu.cn)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text with Feishu document links, status reports, search results, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu document, wiki, drive, and bitable links when operations succeed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
