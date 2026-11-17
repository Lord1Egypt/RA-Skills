## Description:

RAIGO OWASP LLM Top 10 provides agent-readable enforcement rules for the OWASP Top 10 for Large Language Model Applications 2025, covering prompt injection, sensitive information disclosure, supply chain vulnerabilities, excessive agency, and related LLM application risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musharsec](https://clawhub.ai/user/musharsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add OWASP LLM Top 10 aligned deny, warn, and audit rules to OpenClaw agents. It is intended as advisory guardrail text for compliance alignment, not as a complete security product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's protection claims may be read as guaranteed enforcement.

Mitigation: Treat it as advisory guardrail text and confirm the host agent applies the rules as intended.

Risk: Broad refusal language may block legitimate workflows involving sensitive data, tool calls, or multilingual requests.

Mitigation: Review and tune the rule language before deployment in workflows that require those capabilities.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/musharsec/skills/raigo-owasp-top-10-llm)
- [RAIGO OWASP LLM documentation](https://raigo.ai/docs/owasp-llm)
- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown security policy rules with deny, warn, and audit response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only advisory guardrail text; no hidden execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
