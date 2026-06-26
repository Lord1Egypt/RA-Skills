## Description: <br>
OWASP Top 10 AI provides agent-readable OWASP LLM Top 10 (2025) guardrails for OpenClaw agents, with deny, warn, and audit rules for common LLM security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musharsec](https://clawhub.ai/user/musharsec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to add OWASP LLM Top 10-aligned security guardrails to OpenClaw agents. It helps agents identify and respond to prompt injection, sensitive information disclosure, insecure output handling, excessive agency, and related LLM application risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guardrails can produce conservative refusals or confirmation prompts around sensitive data, external tools, generated code execution, system prompt requests, and broad tasks. <br>
Mitigation: Review blocked or warned actions with the user and confirm trusted components, data flow, and task scope before proceeding. <br>
Risk: Separately downloaded organization-specific replacement skills may contain different embedded rules. <br>
Mitigation: Review and scan any replacement skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/musharsec/raigo-owasp-top-10-llm) <br>
- [RAIGO OWASP LLM documentation](https://raigo.ai/docs/owasp-llm) <br>
- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown guidance with deny, warn, and audit response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guardrail skill; no executable code or hidden access found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
