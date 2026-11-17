## Description:

TokenRouter智能词元路由 helps agents evaluate task complexity, recommend L0-L3 model tiers, and provide routing and configuration guidance to balance AI quality with token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent builders use this skill to select cost-effective LLM model tiers, design direct, cascading, or hybrid routing strategies, and produce platform-specific configuration guidance for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain model-routing preferences, budgets, or cost summaries as profile memory.

Mitigation: Confirm the memory/profile behavior before installation and avoid storing sensitive budget or provider-preference details unless that is acceptable.

Risk: Copied provider configuration can send prompts to the external APIs enabled by the user.

Mitigation: Review provider configuration before use and enable only approved API providers, accounts, and keys.

Risk: Model names, availability, and pricing are time-sensitive.

Mitigation: Verify current model names and pricing against official provider documentation before relying on cost estimates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qomob/skills/token-router)
- [Model tiers reference](references/model-tiers.md)
- [Routing strategies guide](references/routing-strategies.md)
- [Configuration templates](references/config-templates.md)
- [Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)
- [OpenAI API pricing](https://openai.com/api/pricing/)
- [Google AI pricing](https://ai.google.dev/pricing)
- [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [xAI model documentation](https://docs.x.ai/docs/models)
- [MiniMax pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo)
- [Microsoft AI pricing](https://microsoft.ai/pricing)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with model recommendations, cost estimates, configuration snippets, and occasional JSON, YAML, or code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English output follows the user's language; model names and pricing should be verified against current provider documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
