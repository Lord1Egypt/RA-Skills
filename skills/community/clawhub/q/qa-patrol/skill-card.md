## Description:

Automated QA testing for web apps using local browser automation, with smoke, auth, payment, data integrity, and static analysis workflows for Supabase/Firebase auth, Stripe payments, React Native Web, Next.js, and SPAs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tahseen137](https://clawhub.ai/user/tahseen137)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to run local browser-based checks against web applications, generate test plans, identify common web app defects, and produce structured QA reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auth, payment, and database checks can submit credentials or database connection values to a configured target application.

Mitigation: Use only staging or disposable targets with unique low-privilege test accounts, and never provide production passwords or production DATABASE_URL values.

Risk: Some templates include delete, storage-clearing, and payment-completion behavior that can modify test data or trigger checkout flows.

Mitigation: Review the selected plan before execution and disable destructive or payment-completion tests unless those actions are intended for the test environment.

Risk: Screenshots, console logs, and QA reports can capture sensitive details from authenticated, payment, or admin screens.

Mitigation: Avoid capturing sensitive screens where possible and redact screenshots or reports before sharing them.

## Reference(s):

- [Qa Patrol Skill Page](https://clawhub.ai/tahseen137/skills/qa-patrol)
- [Test Patterns](references/test-patterns.md)
- [Bug Patterns](references/bug-patterns.md)
- [Report Format](references/report-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with YAML test plans, inline code examples, browser automation steps, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/FAIL/SKIP results, screenshots or screenshot paths, console logs, confidence scoring, SQL snippets, and fix recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
