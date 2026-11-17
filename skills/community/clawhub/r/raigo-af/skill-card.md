## Description:

RAIGO Agent Firewall provides a baseline AI security policy for OpenClaw agents, covering prompt injection, jailbreaks, obfuscation, indirect injection, system prompt extraction, credential exfiltration, destructive commands, code injection, rogue agent detection, goal hijacking, identity spoofing, multi-agent trust exploitation, memory poisoning, supply chain attacks, and related agentic threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musharsec](https://clawhub.ai/user/musharsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to apply a baseline security policy before an OpenClaw agent acts. It helps classify requests into block, confirm, or audit responses for common prompt security and agentic AI threat patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the Markdown policy checklist as a guaranteed security enforcement engine.

Mitigation: Review the skill before deployment and keep agent platform controls, security review, and monitoring in place.

Risk: The optional raigo Cloud upgrade path replaces the local skill with downloaded organisation-specific rules.

Mitigation: Review the replacement SKILL.md and the cloud service privacy and integrity guarantees before using the downloaded policy.

## Reference(s):

- [OpenClaw Integration Guide](https://raigo.ai/docs/openclaw)
- [RAIGO Documentation](https://raigo.ai/docs)
- [raigo Cloud](https://cloud.raigo.ai)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP Top 10 for Agentic AI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-ai-v1-0/)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [ClawHub skill page](https://clawhub.ai/musharsec/skills/raigo-af)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown policy guidance with response templates and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces policy decisions and user-facing block, warning, and audit response guidance; the optional cloud upgrade path can replace the local skill file with organisation-specific rules.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
