## Description: <br>
Call the Kimi API (kimi-k2.6, kimi-k2.5) through RunAPI using the official OpenAI SDK or compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure agents or applications to call Kimi chat models through RunAPI with OpenAI-compatible, Anthropic-compatible, or Gemini-compatible client surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunAPI credentials could be exposed if copied into source files, prompts, shell history, or logs. <br>
Mitigation: Store RunAPI-scoped API keys in environment variables or a secret manager and avoid committing or pasting secrets. <br>
Risk: Prompts may send sensitive or regulated data to the provider flow. <br>
Mitigation: Use this provider path only for data your organization has approved for RunAPI and Kimi processing. <br>


## Reference(s): <br>
- [Kimi model overview](https://runapi.ai/models/kimi.md) <br>
- [Kimi homepage](https://runapi.ai/models/kimi) <br>
- [Moonshot AI provider page](https://runapi.ai/providers/moonshot-ai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-kimi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; requires OPENAI_API_KEY and OPENAI_BASE_URL for use with RunAPI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
