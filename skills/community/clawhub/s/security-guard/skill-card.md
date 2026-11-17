## Description:

Enforces strict handling rules for sensitive information such as API keys, tokens, credentials, PII, and financial data by refusing full disclosure and guiding users toward sanitized snippets or local access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frw1988](https://clawhub.ai/user/frw1988)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide an agent toward conservative responses when handling secrets, credentials, personal data, and financial data. It provides refusal patterns, sanitized-output examples, and local-viewing alternatives for sensitive information requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives itself broad session-wide authority and instructs automatic reads of profile and memory files without clear need or consent.

Mitigation: Review before installing and narrow or remove automatic profile and memory-file reads unless they are explicitly required and consented to.

Risk: Users could mistake the skill for a technical enforcement layer for secrets protection.

Mitigation: Treat it as agent guidance only and keep platform-level controls such as access restrictions, secret scanning, and audit logging in place.

Risk: Passing real secrets to the shell redaction helper can expose them through command history, process listings, or logs.

Mitigation: Avoid using real secrets as command-line arguments; prefer trusted local secret-management tools or test the helper with synthetic values.

## Reference(s):

- [Security Response Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline shell commands and sanitized text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest use of a local shell redaction helper for displaying partial sensitive strings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
