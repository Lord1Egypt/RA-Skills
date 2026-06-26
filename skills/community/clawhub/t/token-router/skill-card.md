## Description: <br>
TokenRouter helps developers and agent builders choose cost-effective LLM model tiers for tasks by scoring complexity, applying safety upgrade rules, and producing routing or configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and cost-conscious AI tool operators use this skill to select model tiers, compare cost and quality tradeoffs, and draft multi-model routing configurations for platforms such as Trae, OpenClaw, Claude Code, Codex CLI, and Hermes Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may infer user preferences from conversation history. <br>
Mitigation: Enable conversation memory only where appropriate, disclose preference tracking to users, and clear or disable the stored profile when it is not needed. <br>
Risk: The skill may activate during cost, model-selection, or routing-adjacent tasks even when the user did not explicitly ask for routing advice. <br>
Mitigation: Review trigger behavior before installation and require user confirmation before changing model choices in unrelated workflows. <br>
Risk: Configuration guidance may involve provider credentials or API routing setup. <br>
Mitigation: Keep API keys out of shared configuration files and use environment variables or a secrets manager for provider credentials. <br>
Risk: Model prices and availability in the reference material can become stale. <br>
Mitigation: Verify provider pricing pages before relying on cost estimates or committing routing budgets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qomob/token-router) <br>
- [README.md](README.md) <br>
- [Model tier reference](references/model-tiers.md) <br>
- [Routing strategies](references/routing-strategies.md) <br>
- [Configuration templates](references/config-templates.md) <br>
- [Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) <br>
- [OpenAI API pricing](https://openai.com/api/pricing/) <br>
- [Google AI pricing](https://ai.google.dev/pricing) <br>
- [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) <br>
- [OpenRouter](https://openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with model tier scores, cost estimates, and optional YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise bilingual Chinese or English responses based on the user's language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
