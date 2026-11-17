## Description:

Persistent memory engine for AI agents with semantic recall, hotness prioritization, importance weighting, time decay, and auto-compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local persistent memory with semantic recall, importance weighting, recency scoring, and compaction to Node.js-based agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can retain sensitive information in MEMORY_STORE.json.

Mitigation: Do not store secrets or credentials, review expected storage behavior before installing, and keep backups of MEMORY_STORE.json.

Risk: Compaction can retain or lose user data in ways users should review first.

Mitigation: Avoid running compaction until the behavior is fixed or clearly accepted, and back up MEMORY_STORE.json before compaction.

## Reference(s):

- [Memory Enhancement Engine API Specification](artifact/references/API_SPEC.md)
- [Memory Enhancement Engine Usage Guide](artifact/references/USE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network output; API and CLI use can create or update a local MEMORY_STORE.json file.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
