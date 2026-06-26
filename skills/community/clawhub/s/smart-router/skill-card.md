## Description: <br>
Expertise-aware model router with semantic domain scoring, context-overflow protection, security redaction, weighted model selection, fallback chains, HITL gates, and cost optimization for Claude, GPT, Gemini, and Grok. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c0nSpIc0uS7uRk3r](https://clawhub.ai/user/c0nSpIc0uS7uRk3r) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to route OpenClaw prompts across configured AI providers based on task intent, context size, provider availability, and risk-related routing rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be automatically routed or retried across configured AI providers. <br>
Mitigation: Review router_config.json, disable providers that should not receive prompts, configure only approved API keys, and use routing visibility for sensitive work. <br>
Risk: Routing metadata may be retained in local router state and logs. <br>
Mitigation: Inspect ~/.openclaw/router-state and ~/.openclaw/logs and manage retained routing metadata according to local data-handling policy. <br>
Risk: Some security claims are not consistently implemented. <br>
Mitigation: Treat redaction and routing controls as safeguards to verify before deployment, especially with representative sensitive prompts. <br>


## Reference(s): <br>
- [A.I. Smart Router on ClawHub](https://clawhub.ai/c0nSpIc0uS7uRk3r/smart-router) <br>
- [Model Reference](references/models.md) <br>
- [Security Reference](references/security.md) <br>
- [Persistent State Notes](STATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses, with optional routing notices and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route or retry prompts across configured Anthropic, OpenAI, Google, and xAI providers; requires python3 and ANTHROPIC_API_KEY, with GOOGLE_API_KEY, OPENAI_API_KEY, and XAI_API_KEY optional.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
