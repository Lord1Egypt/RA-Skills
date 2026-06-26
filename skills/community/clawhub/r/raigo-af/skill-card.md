## Description: <br>
RAIGO Agent Firewall provides an instruction-layer security policy for OpenClaw agents that blocks or flags prompt injection, jailbreak, secret-leakage, destructive-action, and related agent-risk patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musharsec](https://clawhub.ai/user/musharsec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw agents use this skill to add a conservative baseline policy layer before agent actions. It is intended to help agents block, warn on, or audit risky instructions and external-content patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes broad protection claims that may overstate the strength of an instruction-layer policy. <br>
Mitigation: Treat it as a conservative baseline control, review and scan it before deployment, and do not rely on it as a complete security boundary. <br>
Risk: The policy may occasionally overblock legitimate requests. <br>
Mitigation: Test expected workflows before broad rollout and use human confirmation for warn-tier decisions. <br>
Risk: Optional raigo Cloud usage introduces a separate service relationship and audit-logging path. <br>
Mitigation: Review organizational policy, data handling, and compliance requirements before connecting Cloud features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/musharsec/raigo-af) <br>
- [RAIGO OpenClaw Integration Guide](https://raigo.ai/docs/openclaw) <br>
- [RAIGO Documentation](https://raigo.ai/docs) <br>
- [raigo Cloud](https://cloud.raigo.ai) <br>
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [OWASP Top 10 for Agentic AI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-ai-v1-0/) <br>
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown policy responses and decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only policy content; no runtime engine or external calls are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
