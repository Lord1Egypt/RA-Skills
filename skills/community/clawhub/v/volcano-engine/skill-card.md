## Description: <br>
Configure and use Volcano Engine models such as Doubao, GLM, DeepSeek, and Qwen through OpenClaw's OpenAI-compatible provider configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andapeng](https://clawhub.ai/user/andapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Volcengine API credentials, select supported text and multimodal models, define OpenClaw aliases, and troubleshoot authentication or connection issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Volcengine API key and may handle sensitive credentials. <br>
Mitigation: Use a restricted API key, prefer environment variables or a secret manager, and do not commit .env or openclaw.json files containing real keys. <br>
Risk: Connection tests and model prompts are sent to Volcengine remote APIs. <br>
Mitigation: Avoid sending sensitive prompts or files unless you accept Volcengine's data handling terms. <br>
Risk: Token-based remote API use can incur usage costs. <br>
Mitigation: Check official pricing and monitor usage in the Volcano Engine Console before high-volume use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andapeng/volcano-engine) <br>
- [Volcano Engine Official Documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcano Engine API Reference](https://www.volcengine.com/docs/82379/1263693) <br>
- [Volcano Engine Console](https://console.volcengine.com/ark) <br>
- [Volcano Engine Pricing](https://www.volcengine.com/product/ark/pricing) <br>
- [Configuration Guide](references/configuration.md) <br>
- [Models Reference](references/models.md) <br>
- [API Parameters](references/api-parameters.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw provider configuration, model aliases, environment variable guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
