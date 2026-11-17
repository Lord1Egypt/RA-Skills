## Description:

Extracts high-frequency customer questions and best-answer candidates from desensitized customer service conversation logs, then generates a standard FAQ Markdown document and summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

Support operations teams and knowledge-base maintainers use this skill to mine desensitized service logs for recurring customer questions, candidate standard responses, and FAQ content for review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled file reader has a weak path boundary that could expose unintended local files.

Mitigation: Review before installing, run it only on desensitized files you control, and constrain file reading to a dedicated upload directory with canonical path validation before using it in workspaces containing secrets or unrelated private files.

Risk: Customer service logs may contain sensitive customer information if they are not properly prepared.

Mitigation: Use only desensitized logs and have business experts review generated FAQ content before importing it into a knowledge base.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, text]

**Output Format:** [Markdown FAQ document plus plain-text extraction summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [FAQ entries are ordered by question frequency; Excel input support requires Python 3.10+ with pandas and openpyxl/xlrd.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
