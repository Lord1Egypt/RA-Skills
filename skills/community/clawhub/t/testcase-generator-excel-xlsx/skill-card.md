## Description:

Testcase Generator helps agents analyze PRDs against existing case libraries and produce separate Excel workbooks for new and updated test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melissa-lu](https://clawhub.ai/user/melissa-lu)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and product teams use this skill to parse product requirements, identify test scenarios, compare them with configured UHost case libraries, and generate reviewable Excel outputs for new or updated cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured case-library spreadsheets may be updated in place when applying incremental updates.

Mitigation: Back up configured Excel case libraries and review product config paths before running update operations.

Risk: PRD-derived summaries, analyses, and generated workbooks are written under the local OpenClaw workspace.

Mitigation: Use PRDs appropriate for local persistence and review generated files before sharing or opening them in Excel.

Risk: Untrusted PRD content may be carried into generated spreadsheet cells.

Mitigation: Avoid untrusted PRD inputs and inspect generated Excel workbooks before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melissa-lu/skills/testcase-generator-excel-xlsx)
- [Publisher profile](https://clawhub.ai/user/melissa-lu)
- [UHost testcase style reference](references/uhost-testcase-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helpers that write Excel workbooks and PRD-derived notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces new-case and update-case Excel files plus PRD summaries, test-point analysis, and case-comparison notes under the configured workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
