## Description:

Converts PRDs, interface documentation, and requirements specifications into acceptance, integration, testing, and go-live checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Product, engineering, QA, and release teams use this skill to turn written requirements into reviewable Markdown checklists, pending questions, and next-step guidance before acceptance, integration, testing, or launch work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local files selected by the user and can write generated reports to a chosen output path.

Mitigation: Review input paths and output destinations before running the bundled script, and use dry-run or direct Markdown drafting when file writes are not desired.

Risk: Generated checklists may omit requirements or reflect gaps in incomplete PRDs, interface documents, or scope notes.

Mitigation: Treat outputs as review drafts, keep pending questions visible, and verify checklist items against source requirements before execution or release decisions.

Risk: Inputs may contain personal, confidential, or compliance-sensitive information.

Mitigation: Redact sensitive material before processing and keep generated checklist artifacts within the intended local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/spec-to-checklist)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown checklist text, with optional local shell command usage for file-based generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review drafts and checklists from local user-provided inputs; script output can be written to a selected local file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
