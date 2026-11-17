## Description:

SX Self Safety Guard helps agents evaluate runtime request risk and warn, block, or refuse unsafe requests involving prompt injection, impersonation, prompt leakage, excessive agency, supply-chain changes, credential access, malicious code, sensitive data, and anomalous behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxiaobao-y](https://clawhub.ai/user/zhuxiaobao-y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add runtime safety checks and response guidance for security-sensitive requests, including identity claims, prompt-injection attempts, credential access, malicious-code requests, and high-impact agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-decision logging or self-improvement flows could persist raw user requests or quoted attack payloads and later treat them as behavioral instructions.

Mitigation: Configure logging and reflection so raw requests and payloads are not stored as future instructions, require owner approval before lessons affect runtime decisions, and define retention plus rollback controls.

## Reference(s):

- [Identity Verification Protocol](references/identity-verification.md)
- [Prompt Injection Pattern Library](references/prompt-injection-patterns.md)
- [Threat Catalog and Response Templates](references/threat-catalog.md)
- [ClawHub Skill Page](https://clawhub.ai/zhuxiaobao-y/skills/sx-self-safety-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response templates, risk assessments, confirmation prompts, refusal text, and decision-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses L0-L4 risk levels with five-factor scoring and context adjustments.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
