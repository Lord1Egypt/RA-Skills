## Description:

PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to convert local or URL-based PDFs into Markdown for reading, extraction, parsing, summarization, and follow-on analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are uploaded to MinerU's API for processing.

Mitigation: Avoid using the skill for sensitive documents unless the data-sharing terms are acceptable for the intended use.

Risk: The required CLI can be installed from mutable third-party package sources.

Mitigation: Prefer pinned or reviewed CLI versions and scan the installed dependency before deployment.

## Reference(s):

- [Summarize Pdf on ClawHub](https://clawhub.ai/tanis90/skills/summarize-pdf)
- [MinerU homepage](https://mineru.net)
- [MinerU CLI ecosystem page](https://mineru.net/ecosystem?tab=cli)
- [MinerU project](https://github.com/opendatalab/MinerU)
- [mineru-open-api Go install package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main extraction command returns Markdown; tables, formulas, and images may be represented with placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
