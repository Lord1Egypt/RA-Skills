## Description:

Scan source code for security vulnerabilities and suggest fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan source code for common vulnerability patterns, receive severity-oriented findings, and get focused remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pattern-based scanning can miss vulnerabilities or report false positives if treated as a complete audit.

Mitigation: Use the skill as lightweight triage and review findings with normal security testing, code review, and dependency scanning before deployment.

Risk: Scan reports can expose passwords, API keys, tokens, connection string credentials, or sensitive vulnerability details.

Mitigation: Redact actual secret values in all outputs and keep source code, findings, and scan summaries within the current authorized review channel.

Risk: Bundling unrelated cleanup with vulnerability fixes can introduce regressions in untested code paths.

Mitigation: Keep remediation scoped to the vulnerable code and track refactoring or cleanup as separate follow-up work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/security-vuln-scanner-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/security-vuln-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with structured vulnerability findings, severity labels, security scores, and focused remediation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan output should redact actual secret values, avoid external transmission of findings, and keep fixes scoped to vulnerable code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
