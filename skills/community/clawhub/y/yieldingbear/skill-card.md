## Description: <br>
Yielding Bear's unified LLM API helps agents route LLM requests across multiple providers for cost arbitrage and intelligent routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yieldingbear](https://clawhub.ai/user/yieldingbear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure OpenClaw agents, custom scripts, or OpenAI-compatible clients to send LLM requests through Yielding Bear for cost-aware provider routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, files, or business content may be submitted to Yielding Bear and routed model providers. <br>
Mitigation: Use the skill only when policy allows the provider flow, and avoid sending secrets, regulated data, or confidential customer/business content unless approved. <br>
Risk: API keys can be exposed if permanently written into shell profiles or shared command history. <br>
Mitigation: Prefer a secret manager, OS keychain, or temporary environment variable for YIELDINGBEAR_API_KEY. <br>


## Reference(s): <br>
- [Yielding Bear API docs](https://yieldingbear.com/developers) <br>
- [Yielding Bear API key](https://yieldingbear.com/api) <br>
- [Yielding Bear yields](https://yieldingbear.com/yields) <br>
- [How Yielding Bear works](https://yieldingbear.com/how-it-works) <br>
- [Yielding Bear dashboard](https://yieldingbear.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Yielding Bear API key and sends prompts to a third-party routing API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
