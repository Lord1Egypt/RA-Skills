## Description:

Cost-optimize AI agent operations by routing tasks to appropriate models based on complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigabit-eth](https://clawhub.ai/user/gigabit-eth)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use SwitchBoard to classify agent tasks by complexity and choose cost-appropriate OpenRouter models for main sessions, sub-agents, and automated jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts routed through OpenRouter models may be logged or used by some providers, especially free or unmoderated models.

Mitigation: Avoid routing secrets, API keys, passwords, or private PII through free or unmoderated models, and review model privacy policies before use.

Risk: The skill depends on an OpenRouter API key and external model availability, so routing commands can fail when credentials, rate limits, or provider availability are unsuitable.

Mitigation: Configure the OpenRouter API key knowingly, monitor provider status and rate limits, and keep a default model available for fallback.

Risk: Server security guidance notes that the listed repository and homepage do not clearly match the skill.

Mitigation: Verify the publisher profile and source links before relying on the release in sensitive workflows.

## Reference(s):

- [OpenRouter Models Reference](references/openrouter-models.md)
- [OpenRouter Models Catalog](references/openrouter-models.json)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [ClawHub Skill Page](https://clawhub.ai/gigabit-eth/skills/router)
- [Publisher Profile](https://clawhub.ai/user/gigabit-eth)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with JSON, YAML, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides model-tier recommendations and routing guidance; it does not contain executable code.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
