## Description:

Textin Parse helps an agent send images, PDFs, Office documents, HTML, text, and similar files to the Textin document parsing API for OCR, layout analysis, table and formula recognition, and Markdown or structured-data output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingjus](https://clawhub.ai/user/kingjus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to configure Textin API credentials and parse supported documents into Markdown and structured results for document conversion, content extraction, table recognition, formula recognition, and outline extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends uploaded documents or document URLs to Textin for parsing.

Mitigation: Use it only with documents approved for that provider, and avoid sensitive or regulated files unless policy allows Textin processing.

Risk: The skill stores Textin API credentials in a local config file.

Mitigation: Do not paste long-lived secrets into chat; rotate credentials already used with the skill and restrict the config file permissions manually after installation.

Risk: The shell parser has weak safeguards for untrusted filenames.

Mitigation: Prefer trusted filenames or the Python parser until the shell curl argument handling is fixed.

## Reference(s):

- [Textin Parse ClawHub page](https://clawhub.ai/kingjus/skills/textin-parse)
- [Textin registration](https://www.textin.com/register/code/3EJS7P)
- [Textin document parsing API endpoint](https://api.textin.com/ai/service/v1/pdf_to_markdown)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown text by default, with optional JSON results and shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Textin API credentials; supports local files or URLs up to 500MB and parser options for mode, tables, images, formulas, charts, page ranges, and output files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.yaml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
