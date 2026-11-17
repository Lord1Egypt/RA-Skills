## Description:

Software IP self-assessment for Chinese software copyright applications, including material completeness checks, source code documentation audit prompts, user manual review, rights attribution verification, registration readiness assessment, and payment verification through clawtip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and software copyright applicants use this skill to receive a Chinese-language readiness review before preparing or submitting Chinese software copyright registration materials. It helps identify missing materials, documentation issues, rights attribution concerns, and remediation steps after local payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions are stored locally under the user's home directory and may contain sensitive source code, applicant details, trade secrets, or ownership facts.

Mitigation: Keep the initial question minimal and avoid including sensitive materials unless local cleartext storage is acceptable.

Risk: Payment authorization is based on local order and credential files and should not be treated as strong proof of payment.

Mitigation: Use this package's payment status only as a local workflow gate and rely on the official clawtip payment flow for payment handling.

Risk: The documented sandbox payment command executes an npx package at runtime.

Mitigation: Run the sandbox payment command only in a contained environment after reviewing the package and command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/soft-ip-full-lifecycle-zijian-clawhub-reviewfix)
- [Publisher profile](https://clawhub.ai/user/jinyu12166)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational assessment report with shell command output and JSON status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese-language compliance review guidance delivered after local order and payment checks.]

## Skill Version(s):

3.1.38 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
