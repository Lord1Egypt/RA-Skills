## Description:

ManualExpert translates hardware and technical manuals into complete page-by-page bilingual Markdown tables and can export them to Word for DTP preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mugeng-su](https://clawhub.ai/user/mugeng-su)

### License/Terms of Use:

MIT-0

## Use Case:

External translators, localization teams, and technical documentation teams use this skill to translate hardware and technical manuals while preserving page breaks, source text, terminology consistency, and bilingual review structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source manuals may contain confidential or restricted technical content that would be exposed to the agent during extraction and translation.

Mitigation: Confirm the manuals can be shared with the agent before use and avoid submitting content outside the intended translation workflow.

Risk: The included DOCX export script reads a Markdown input path and writes to a user-specified output path.

Mitigation: Run the export script only on Markdown files and output paths selected by the user.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown bilingual tables with optional Word .docx export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves page-by-page structure and source/target text pairs; Word export depends on the included Python script and python-docx.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
