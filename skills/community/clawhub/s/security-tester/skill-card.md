## Description:

Security Tester helps agents test web application and API security against OWASP guidance by generating vulnerability test cases, analyzing scan results, and drafting security test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and authorized application testers use this skill to plan OWASP-aligned web and API security tests, document findings, and produce remediation-oriented reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes exploit-style web and API test commands that may disrupt systems or exceed authorization if used outside an approved scope.

Mitigation: Use it only on systems you own or are explicitly authorized to test, define the exact target scope before execution, and prefer staging environments and test accounts.

Risk: Some example payloads and probes may be destructive, resource-intensive, or directed at sensitive cloud metadata endpoints.

Mitigation: Avoid destructive payloads and cloud metadata probes unless separately approved, and set conservative request limits for all testing.

Risk: Security testing output may expose tokens, credentials, personal data, or configuration details in logs and reports.

Mitigation: Redact sensitive values from command output, logs, and reports before sharing or retaining results.

## Reference(s):

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [FIRST CVSS](https://www.first.org/cvss/)
- [OWASP Top 10 Detailed Test Procedures](references/owasp-top10-tests.md)
- [API Security Testing](references/api-security.md)
- [ClawHub Skill Page](https://clawhub.ai/zhanghengyi1986-afk/skills/security-tester)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhanghengyi1986-afk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vulnerability test procedures, CVSS scoring guidance, and security report content.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
