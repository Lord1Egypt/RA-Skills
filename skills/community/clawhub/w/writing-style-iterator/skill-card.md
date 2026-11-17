## Description:

Writing Style Iterator helps an agent load, apply, and iteratively update a user's writing style rules for writing, rewriting, polishing, tone adjustment, and translation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanjiaming](https://clawhub.ai/user/shanjiaming)

### License/Terms of Use:


## Use Case:

External users and writing-focused agent workflows use this skill to preserve personal writing preferences, apply them to new drafts, and learn from edits or feedback across iterative writing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent local copies of drafts and inferred style rules.

Mitigation: Use it only for documents whose retention is acceptable, and add clear purge controls or retention limits before applying it to confidential, regulated, credential-bearing, or shared documents.

Risk: The skill automatically updates style rules and draft history with limited user control.

Mitigation: Require explicit approval before file writes or commits, review diffs before applying changes, and keep rollback instructions available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanjiaming/skills/writing-style-iterator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local style rules and draft snapshots when the workflow is followed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
