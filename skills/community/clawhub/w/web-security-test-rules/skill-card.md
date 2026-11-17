## Description:

Provides rules and checklists for authorized web application security testing, emphasizing authorization, low-impact testing, restoration, scope control, and structured reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT

## Use Case:

Developers, security testers, and authorized assessors use this skill to plan and conduct scoped web application security testing, maintain evidence of authorization, minimize operational impact, and produce findings reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented bypass switches can weaken authorization, destructive-action, and third-party-scope controls.

Mitigation: Review before installing, prefer signed AUTHORIZATION.json, avoid auth.disable and MOWEN_AUTH_OVERRIDE bypasses, and require separate written scope for destructive or third-party tests.

Risk: Security testing reports can contain sensitive target, account, request, or vulnerability details.

Mitigation: Keep reports in a private authorized location and redact sensitive data before sharing or archiving.

Risk: Destructive testing can change or delete target resources when authorization scope or backups are incomplete.

Mitigation: Require explicit destructive-operation authorization, create recoverable backups first, record backup locations, and stop if any action exceeds the authorized scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mowenqwq/skills/web-security-test-rules)
- [Authorization template](references/authorization_template.json)
- [Authentication and credential notes](references/auth_notes.md)
- [Destructive-operation backup notes](references/backup_notes.md)
- [Security report template](references/report_template.md)
- [Trusted public-key management](references/authorized_pubkeys/README.md)
- [Authorization signing helper](scripts/sign_auth.sh)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, JSON authorization templates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce security test plans, authorization checks, operation logs, and findings reports for explicitly authorized targets.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
