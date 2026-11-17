## Description:

Prototype OpenClaw skill that reads SNS-style comments from a local text file or local HTTP test page, detects RSFPH watermarks with detect_watermark.py, and appends only watermark-detected comments to MEMORY.md as category-organized topic summaries.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[llevm](https://clawhub.ai/user/llevm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use SNSwatcher to test the IBIA watermark-memory prototype or turn local SNS-style comments into category-organized notes in OpenClaw memory. It filters for detected watermarks and supports previewing changes before appending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watermark detection does not establish that a comment is trustworthy; saved third-party claims may influence future agent responses.

Mitigation: Use controlled comment sources, review the proposed note with --dry-run before writing, and remove the appended block to undo an update.

Risk: Normal execution makes persistent changes by appending to MEMORY.md.

Mitigation: Preview with --dry-run and inspect the printed block before allowing a normal run to append it.

## Reference(s):

- [SNSwatcher ClawHub release](https://clawhub.ai/llevm/skills/skill-test-v4)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown memory-note block with plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only watermark-detected comments are included; normal runs append a self-contained block to MEMORY.md, while --dry-run previews without writing. Topic and summary fields are limited to 300 characters each.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
