## Description:

Refines raw reading notes by merging similar ideas, removing noise, and summarizing key points into MkDocs Material-style Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smilingwayne](https://clawhub.ai/user/smilingwayne)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge-base maintainers use this skill to turn scattered reading or study notes into structured, high-density MkDocs Material-style Markdown. It supports category confirmation, semantic clustering, user-approved reconstruction, and completion reporting for traceability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rewrite, merge, or omit material while producing a refined copy.

Mitigation: Review the generated refinement plan before approval and check the final refined Markdown against the source notes.

Risk: The skill writes plan, refined output, and backup files near the selected note file.

Mitigation: Use it on intended note files and confirm the expected output locations before proceeding.

## Reference(s):

- [Notes by Category](references/notes_classify.md)
- [ClawHub Skill Page](https://clawhub.ai/smilingwayne/skills/refine-markdown-to-mkdocs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown plan, refined Markdown notes, and completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a refinement plan file, a refined note file, backups, and deletion summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
