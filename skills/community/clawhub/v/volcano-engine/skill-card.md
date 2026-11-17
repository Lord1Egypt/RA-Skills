## Description:

Configure and use Volcano Engine (Volcengine) models including Doubao, GLM, DeepSeek, and Qwen through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andapeng](https://clawhub.ai/user/andapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Volcengine API access in OpenClaw, choose text or multimodal models, set model aliases, and troubleshoot authentication or connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, and API credentials may be sent to Volcengine when this provider is configured.

Mitigation: Use the skill only when Volcengine model support is needed, store credentials in environment variables or a protected credential store, and restrict and rotate API keys.

Risk: Optional documentation-updater or crawler steps may run recurring background automation or unpinned npm/npx tooling.

Mitigation: Do not enable those optional updater or crawler steps unless they have been reviewed, pinned, and run in a contained environment.

## Reference(s):

- [Volcengine Skill Page](https://clawhub.ai/andapeng/skills/volcano-engine)
- [Volcano Engine Official Documentation](https://www.volcengine.com/docs/82379)
- [Volcano Engine API Reference](https://www.volcengine.com/docs/82379/1263693)
- [Volcano Engine Console](https://console.volcengine.com/ark)
- [Volcano Engine Pricing](https://www.volcengine.com/product/ark/pricing)
- [Configuration Guide](references/configuration.md)
- [Models Reference](references/models.md)
- [API Parameters Reference](references/api-parameters.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown]

**Output Format:** [Markdown with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model IDs, endpoint URLs, API-key environment variable names, and troubleshooting steps.]

## Skill Version(s):

1.1.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
