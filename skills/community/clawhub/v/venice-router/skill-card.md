## Description:

Routes prompts to Venice.ai text models by classifying task complexity, selecting cost-aware tiers, and supporting streaming, web search, conversation context, tool calls, and model preference flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plusone](https://clawhub.ai/user/plusone)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to send prompts through Venice.ai with automatic or explicit model-tier routing, budget-aware selection, web search, conversation history, and function-calling support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy and private-only controls are over-promised and may expose sensitive prompts when routing or explicit model overrides select non-private models.

Mitigation: Review before confidential use, avoid premium or explicit model overrides for sensitive prompts, and do not treat private-only settings as a hard guarantee in this version.

Risk: Web search, conversation files, and tool definitions may send local data to external services.

Mitigation: Disable web search for sensitive work, review conversation and tool files before use, and remove secrets or confidential content before routing.

Risk: Budget settings are soft routing guidance and may not fully prevent unexpected API costs.

Mitigation: Use provider-side quotas or billing alerts, check budget status, and classify prompts before sending expensive requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/plusone/skills/venice-router)
- [Publisher Profile](https://clawhub.ai/user/plusone)
- [Source Homepage](https://github.com/PlusOne/venice.ai-router-openclaw)
- [Venice.ai](https://venice.ai)
- [Venice.ai Documentation](https://docs.venice.ai)
- [Venice.ai Model Reference](references/models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from the Venice.ai router, with Markdown, code, shell commands, and configuration guidance depending on the selected model response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream responses, return tool-call metadata, emit routing details, and record local cost-tracking data.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
