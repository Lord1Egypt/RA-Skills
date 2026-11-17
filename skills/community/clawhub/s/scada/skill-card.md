## Description:

Scada provides shell commands for a local file-based record manager presented as a supervisory control and data acquisition manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to run local CLI commands that add, list, search, remove, export, and summarize records stored under a configurable data directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled as a SCADA tool, but security evidence identifies it as a local notes/configuration tool rather than an industrial SCADA integration.

Mitigation: Do not use it to control or monitor industrial systems; review the commands as local record-management utilities only.

Risk: Security evidence reports unsafe shell input handling that can lead to command execution.

Mitigation: Review before installing, avoid untrusted config/search/export input, and fix command construction and escaping before relying on the skill.

Risk: CSV and JSONL exports may contain unescaped user-provided values.

Mitigation: Inspect exported files before opening them in spreadsheet tools or downstream automation.

## Reference(s):

- [Scada Skill Page](https://clawhub.ai/xueyetianya/skills/scada)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output, JSONL data, and optional JSON or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data in ~/.scada/ by default or in SCADA_DIR when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
