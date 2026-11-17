## Description:

Read and parse XML from construction systems - P6 schedules, BSDD exports, IFC-XML, COBie-XML. Convert to pandas DataFrames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data practitioners and developers use this skill to parse XML exports from P6 schedules, IFC-XML, COBie-XML, and buildingSMART Data Dictionary into structured tables for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires filesystem access to construction data files.

Mitigation: Grant access only to intended project files and review file paths before parsing.

Risk: Very large or deeply nested XML inputs can create parser-hardening and reliability issues.

Mitigation: Use trusted XML inputs where possible and validate file size and nesting depth before processing.

Risk: CSV, Excel, and JSON support is mentioned as informal output handling rather than explicit parser behavior.

Mitigation: Treat non-XML formats and exports as convenience outputs that require user review before relying on them.

## Reference(s):

- [Data Driven Construction Homepage](https://datadrivenconstruction.io)
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/xml-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code examples and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May present parsed XML elements as pandas DataFrame-style tables and suggest CSV, Excel, or JSON exports.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
