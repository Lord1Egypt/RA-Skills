## Description:

Automatically downloads Young Post Club Spark articles, creates HTML and PDF study materials, and can upload generated files to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch Young Post Club Spark article lists, collect article content, generate HTML and PDF learning materials, and optionally upload the generated files to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe shell execution in the PDF conversion path.

Mitigation: Review the scripts before installing and replace shell-string execution with subprocess calls that pass arguments as a list.

Risk: Generated HTML and PDF output may include fetched article content that has not been sanitized.

Mitigation: Sanitize article titles, URLs, and body content before rendering HTML or converting it to PDF.

Risk: The Feishu upload behavior is under-scoped and may upload generated files without enough user confirmation.

Mitigation: Require explicit approval and a reviewed destination before uploading files to Feishu.

Risk: The security scan describes the current scripts as incomplete and not production-ready automation.

Mitigation: Treat the skill as review-required before deployment and validate output paths, network behavior, and error handling in a controlled workspace.

## Reference(s):

- [Young Post Club Spark](https://www.youngpostclub.com/spark)
- [ClawHub Skill Page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/young-post-downloader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts are HTML and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch website content, render local HTML/PDF files, and upload generated files to Feishu when enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
