## Description:

Smart Memory (Zero Dep) helps an agent maintain local working and long-term memory through session state, daily notes, memory type classification, extraction prompts, and decay or archival workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgjq](https://clawhub.ai/user/zgjq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve task state, extract durable conversation memories, organize memory files by type, and run maintenance such as classification, promotion, health checks, and archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation data into local memory files.

Mitigation: Use it only in a private workspace, require explicit user opt-in for automatic extraction, and avoid storing secrets, credentials, private third-party conversations, or information the user asked not to remember.

Risk: Session restore can overwrite current memory state.

Mitigation: Review and validate snapshot files before restore, and limit restore operations to expected snapshot paths.

Risk: The session cache uses /tmp and the health script inspects /tmp cache files.

Mitigation: Harden temporary-file permissions and avoid shared-machine use until cache and health-script handling are reviewed.

Risk: Saved memories may later be read by an agent and influence behavior.

Mitigation: Treat memory contents as untrusted data and review them before using them as operational instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgjq/skills/smart-memory-zero-dep)
- [Memory Schema Reference](artifact/references/memory_schema.md)
- [Decay & Archival Rules](artifact/references/decay_rules.md)
- [Memory Extraction Prompt Template](artifact/references/extraction_prompt.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and reports; no external dependencies or network calls are described in the artifact.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
