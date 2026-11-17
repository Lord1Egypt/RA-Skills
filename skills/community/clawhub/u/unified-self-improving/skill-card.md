## Description:

Unified Self Improving helps agents manage self-improvement memory through structured logging, HOT/WARM/COLD storage, namespace isolation, indexing, imports, session lifecycle commands, and repeated pattern detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[421zuoduan](https://clawhub.ai/user/421zuoduan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist corrections, errors, patterns, and session learnings so an agent can query, recall, promote, archive, and index its own operational memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File path handling can escape intended storage boundaries and delete or overwrite local data.

Mitigation: Review before installing, use only trusted IDs and namespace names, keep backups of the memory root, and add path containment checks plus strict ID and namespace validation before broader use.

Risk: Untrusted JSONL imports or persisted prompts can introduce unsafe or sensitive memory content.

Mitigation: Import only trusted JSONL, avoid storing secrets or sensitive prompts, and add schema and provenance checks for imported records.

Risk: Namespace deletion and automatic persistence actions can remove or retain data unexpectedly.

Mitigation: Require clear confirmation for destructive actions and review automatic session-end persistence behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/421zuoduan/skills/unified-self-improving)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSONL memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local Markdown, JSONL, index, namespace, and session files under the configured memory root.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
