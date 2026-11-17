## Description:

Generates comprehensive test case documents from requirements, product specifications, or feature descriptions, with Markdown output by default and optional XMind mind map output when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duyinghua](https://clawhub.ai/user/duyinghua)

### License/Terms of Use:

MIT-0

## Use Case:

Testers, product managers, and developers use this skill to turn textual requirements into structured, detailed test case documents for review and execution. It is most useful when requirements need broad functional, boundary, exception, compatibility, performance, and security coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional XMind converter uses a shared temporary folder and may overwrite or remove local files in some environments.

Mitigation: Use the Markdown-only workflow by default, or change the converter to use a unique secure temporary directory before running it on shared machines or automation accounts.

Risk: Requirement document URLs may expose private data access because the skill may read or download their contents.

Mitigation: Review document permissions and avoid providing sensitive requirement URLs unless the execution environment is approved for that data.

## Reference(s):

- [Test case document format guide](references/testcase_template.md)
- [Requirements analysis guide](references/analysis_guide.md)
- [Test case quality standard](references/quality_standard.md)
- [Functional module merge guide](references/module_merge_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown test case document, optional XMind file, and concise textual summary with coverage statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files use timestamped names; XMind output is generated only when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
