## Description: <br>
Pura routes OpenClaw agent LLM requests through an OpenAI-compatible gateway that selects lower-cost or premium providers based on request complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[espetey](https://clawhub.ai/user/espetey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure an agent to send chat-completion requests through Pura for automatic provider routing, cost reporting, and optional wallet-related account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent prompts and responses are routed through Pura and may be sent to downstream providers such as Groq, Gemini, OpenAI, or Anthropic. <br>
Mitigation: Use the skill only when that routing is acceptable for the data being processed. <br>
Risk: PURA_API_KEY is a real credential, and setup or verification output can reveal enough information to misuse it. <br>
Mitigation: Keep the key secret, avoid sharing command output, and rotate the key if it is exposed. <br>
Risk: Report and wallet commands access billing, spend, balance, or funding-related account functions. <br>
Mitigation: Review those commands and their responses before running or acting on them. <br>


## Reference(s): <br>
- [Pura website](https://pura.xyz) <br>
- [Pura documentation](https://pura.xyz/docs) <br>
- [Pura cascade routing comparison](https://pura.xyz/compare) <br>
- [Pura API gateway](https://api.pura.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash, Python, curl, and JSON examples; helper scripts output text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PURA_API_KEY; PURA_GATEWAY_URL is optional for overriding the gateway endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
