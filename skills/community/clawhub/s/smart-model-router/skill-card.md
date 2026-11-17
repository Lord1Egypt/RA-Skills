## Description:

TinkerClaw Model Router is a billing-aware guide for choosing among models already configured in an OpenClaw setup for agent, sub-agent, or cron tasks while preferring flat-rate or free options unless metered use is justified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to select an appropriate configured model tier for interactive work, sub-agents, and cron jobs while respecting budget pressure and avoiding unnecessary metered spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The routing policy can influence which configured model handles future agent, sub-agent, or cron work.

Mitigation: Review the routing preferences and budget thresholds before installation; add the persistent AGENTS.md snippet only when this policy should apply across sessions.

Risk: If the optional local classifier is enabled, a task summary is sent to a local loopback model for tier selection.

Mitigation: Leave MODEL_ROUTER_CLASSIFIER unset unless local classification is intended, and use only an abstract task summary without code, credentials, names, URLs, customer data, or personal data.

## Reference(s):

- [TinkerClaw Model Router on ClawHub](https://clawhub.ai/globalcaos/skills/smart-model-router)
- [Model Strengths Reference](references/model-strengths.md)
- [Task Orchestration Patterns](references/task-orchestration.md)
- [Chain-of-Thought Reasoning Techniques](references/chain-of-thought.md)
- [model-prompt-adapter](https://clawhub.ai/globalcaos/model-prompt-adapter)
- [subagent-overseer](https://clawhub.ai/globalcaos/subagent-overseer)
- [agent-superpowers](https://clawhub.ai/globalcaos/agent-superpowers)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with routing tables, code examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model tier and model-selection guidance; the skill is instruction-only and does not act as a runtime proxy.]

## Skill Version(s):

2.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
