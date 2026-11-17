## Description:

Expertise-aware model router with semantic domain scoring, context-overflow protection, and security redaction for selecting among Claude, GPT, Gemini, and Grok models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0nspic0us7urk3r](https://clawhub.ai/user/c0nspic0us7urk3r)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to route prompts across configured model providers based on intent, complexity, context size, fallback availability, and cost considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts can be silently routed to external model providers.

Mitigation: Use explicit provider allowlists and require user confirmation before cross-provider routing, especially for sensitive or proprietary material.

Risk: The shipped executable delegation path bypasses the promised credential filter.

Mitigation: Enforce a single sanitization path for all delegation and fallback flows before allowing live routing.

Risk: Sensitive data may be exposed if routed to providers without an approved data policy.

Mitigation: Avoid using the skill with secrets, health data, financial records, customer data, or proprietary material unless additional policy controls are added.

## Reference(s):

- [A.I. Smart Router on ClawHub](https://clawhub.ai/c0nspic0us7urk3r/skills/smart-router)
- [Model Capabilities & Pricing Reference](artifact/references/models.md)
- [Security Best Practices for Model Routing](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional routing notices, status output, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route prompts to configured external model providers and may include model attribution or fallback notices when routing visibility is enabled.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
