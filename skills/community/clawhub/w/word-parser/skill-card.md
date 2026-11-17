## Description:

Parses and extracts structured content from Word documents (.docx and .doc) using the MinerU API and mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to parse Word files into structured content for indexing, document analysis, form extraction, and report automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word documents may be processed through MinerU or a third-party CLI outside the local environment.

Mitigation: Use only documents approved for external processing and follow organizational data-handling policy.

Risk: The skill installs and runs the third-party mineru-open-api package.

Mitigation: Confirm trust in the package and service, and prefer a pinned or isolated install before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; parsed document outputs are produced by mineru-open-api as structured JSON and files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick .docx parsing without a token and deeper extraction for tables, formulas, and JSON output when configured.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
