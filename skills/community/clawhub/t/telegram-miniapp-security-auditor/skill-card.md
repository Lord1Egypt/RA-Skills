## Description:

Audits Telegram Mini App projects for launch-readiness risks around initData validation, bot tokens, admin endpoints, CORS, PII collection, and public channel deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a static, evidence-first audit of Telegram Mini App projects before connecting production bot tokens, BotFather settings, or public channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a user-selected Telegram Mini App project, which can include local configuration files such as .env.

Mitigation: Run it only on projects you intend to audit and review report contents before sharing them.

Risk: Generated audit reports may contain token-like or secret-like snippets from the scanned project.

Mitigation: Store reports in a private location and redact sensitive snippets before distributing results.

## Reference(s):

- [Telegram Mini App Security Checklist](references/tma-security-checklist.md)
- [Project homepage](https://github.com/zack-dev-cm/telegram-miniapp-security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON audit reports with concise launch recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, evidence snippets, PASS/REVIEW/BLOCK decisions, and remediation guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
