## Description:

Parse and analyze STDF (Standard Test Data Format) semiconductor test files. Convert STDF to CSV/XLSX, generate analysis reports, correlation reports, PDF charts, and extract specific test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showjim](https://clawhub.ai/user/showjim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and semiconductor test engineers use this skill to run the STDF Reader CLI for converting STDF files, extracting test records, and producing CSV, XLSX, and PDF analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation and execution of an external Python CLI package.

Mitigation: Install the package in a dedicated virtual environment under a non-privileged account, and consider pinning and reviewing the stdf-reader package version before use.

Risk: Generated CSV, XLSX, and PDF files default to the input file directory unless an output path is specified.

Mitigation: Choose explicit output paths when handling sensitive STDF data or when preserving the input directory matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showjim/skills/stdf-reader)
- [Publisher profile](https://clawhub.ai/user/showjim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to produce or request STDF Reader outputs such as CSV, XLSX, PDF, and extracted record files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
