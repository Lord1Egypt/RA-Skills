## Description: <br>
Provides structured, quantifiable functional test case review across completeness, accuracy, effectiveness, executability, standards compliance, and maintainability, with reports, missing-scenario suggestions, dependency analysis, and improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxpfreesky](https://clawhub.ai/user/zxpfreesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test leads, and development teams use this skill to review functional test cases against requirements, quantify quality gaps, and produce actionable Markdown review reports before execution or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review output can be incomplete or unreliable when the user omits the requirements document or test cases. <br>
Mitigation: Require both inputs before starting the review and ask the user to supply any missing artifact. <br>
Risk: The skill may produce incorrect or misleading quality guidance if requirement interpretation or business context is wrong. <br>
Mitigation: Have QA or product reviewers confirm high-severity findings, coverage gaps, and scoring before using the report as a quality gate. <br>
Risk: Security evidence reports no hidden malware or exfiltration, but installation should still be deliberate. <br>
Mitigation: Review the skill artifacts and only install from the server-resolved ClawHub release and publisher profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zxpfreesky/testcase-reviewer) <br>
- [Publisher Profile](https://clawhub.ai/user/zxpfreesky) <br>
- [Test Case Review Report Template](artifact/report/测试用例评审报告模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review report with scoring tables, issue lists, traceability matrix, missing-scenario suggestions, dependency analysis, and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires both a requirements document and test cases before review begins.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
