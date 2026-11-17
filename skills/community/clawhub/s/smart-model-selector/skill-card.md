## Description:

Smart Model Selector automatically recommends a Qwen model for each task, using rule-based routing and local feedback history to balance task fit and cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billhandsome52](https://clawhub.ai/user/billhandsome52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route prompts among qwen3.5-plus, qwen-max, and qwen-coder-plus, with commands for manual override, ratings, reset, and usage statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rated sessions can persist full prompt text and model-selection metadata in a local plaintext SQLite database.

Mitigation: Avoid rating or recording sensitive chats, delete the documented model_selection.db when retention is not desired, and prefer a future no-logging or derived-feature-only mode for sensitive environments.

Risk: The skill injects model-selection guidance into the agent context and may affect model choice without changing the underlying model itself.

Mitigation: Review recommendations before relying on them for high-impact work and use the manual model override command when a specific model is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billhandsome52/skills/smart-model-selector)
- [Publisher profile](https://clawhub.ai/user/billhandsome52)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style injected context and command replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides model recommendations, selection reasons, manual override confirmations, ratings feedback, reset responses, and usage statistics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
