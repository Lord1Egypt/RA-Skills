## Description: <br>
QA Patrol provides local browser automation for web app QA across smoke, auth/payment, static analysis, and database integrity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tahseen137](https://clawhub.ai/user/tahseen137) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run local QA checks against web applications, including smoke tests, authentication and payment flows, data integrity comparisons, and static analysis for known web app bug patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation and advanced QA checks can interact with real application state. <br>
Mitigation: Run the skill against staging apps with synthetic data, disposable test accounts, and Stripe test mode. <br>
Risk: Level 3 checks can require local repo read access or a user-provided database connection. <br>
Mitigation: Grant Level 3 access only when needed, prefer read-only or disposable database credentials, and avoid production DATABASE_URL values. <br>
Risk: Screenshots, console logs, and reports can contain sensitive application data. <br>
Mitigation: Review, secure, or delete generated evidence after use. <br>


## Reference(s): <br>
- [QA Patrol ClawHub release](https://clawhub.ai/tahseen137/qa-patrol) <br>
- [Test Patterns](references/test-patterns.md) <br>
- [Bug Patterns](references/bug-patterns.md) <br>
- [QA Report Format](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with YAML test plans and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser snapshots, console findings, screenshots, pass/fail tables, confidence scores, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
