## Description:

Testcase Reviewer provides a Chinese-language, structured review of functional test cases against requirements, covering completeness, accuracy, validity, executability, standards compliance, and maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxpfreesky](https://clawhub.ai/user/zxpfreesky)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, testers, and development teams use this skill to review functional test cases against requirements, quantify quality across six dimensions, and receive missing-scenario, dependency, and improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated report may overwrite an existing report if the project or module name resolves to the same output filename.

Mitigation: Confirm the intended report path before running the skill in a shared repository.

Risk: Review results are unreliable if either the requirements document or the test cases are missing.

Mitigation: Provide both required inputs before starting the review.

## Reference(s):

- [Test Case Review Report Template](artifact/report/测试用例评审报告模板.md)
- [ClawHub skill page](https://clawhub.ai/zxpfreesky/skills/testcase-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with scoring tables, traceability matrix, issue lists, missing-scenario suggestions, dependency analysis, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects both requirements and test cases as inputs before review; generated reports should be written to the configured report location without overwriting existing reports.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
