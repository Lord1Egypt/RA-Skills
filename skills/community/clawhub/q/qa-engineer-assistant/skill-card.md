## Description: <br>
This skill helps QA and test engineers understand requirements, design test cases, generate API and UI automation scripts, create bug reports, and guide junior testers through testing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guolongganga](https://clawhub.ai/user/guolongganga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test engineers, and developers use this skill to turn requirements or bug descriptions into structured test cases, API/UI automation examples, bug reports, and next-step testing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API tests can execute real network requests and may use authentication tokens or test credentials. <br>
Mitigation: Use dedicated low-privilege test accounts or CI secrets, avoid unintended production targets, and review generated tests before running them. <br>
Risk: API responses, logs, or generated assertions may expose tokens, cookies, passwords, or personal data. <br>
Mitigation: Avoid logging full sensitive responses and redact secrets or personal data from bug reports and shared test artifacts. <br>


## Reference(s): <br>
- [QA Engineer Assistant on ClawHub](https://clawhub.ai/guolongganga/qa-engineer-assistant) <br>
- [API Test Guide](references/api-test-guide.md) <br>
- [Bug Report Template](references/bug-report-template.md) <br>
- [Test Case Template](references/test-case-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, checklists, and fenced Python or shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should end with next-step recommendations and may include beginner-friendly Chinese comments for generated scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
