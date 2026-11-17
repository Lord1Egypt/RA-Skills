## Description:

Travelogue Weaver helps users record trip moments with text and media, organize them into timelines, generate narrative travelogues, and export Markdown, HTML, or PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage a travel journal lifecycle, capture multimedia trip moments, generate a readable travelogue, and export it for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read uploaded file paths and persist private location and media metadata.

Mitigation: Run it in a constrained workspace and avoid passing arbitrary local paths.

Risk: The skill can write exports and may produce unsafe HTML output.

Mitigation: Review generated exports before sharing or opening them in sensitive environments.

Risk: Trip-ending and delete actions can affect saved travel records.

Mitigation: Require explicit user confirmation before delete or trip-ending actions.

## Reference(s):

- [Data model definition](references/data_model.md)
- [Export format specification](references/export_format.md)
- [Narrative style guide](references/narrative_guide.md)
- [ClawHub skill page](https://clawhub.ai/ludiansheng/skills/travelogue-weaver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown, HTML, PDF, JSON state files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local travel records and uploaded media under travelogue_data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
