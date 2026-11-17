## Description:

Optimize API costs by routing tasks to cost-effective models through PaleBlueDot AI TokenRouter, using live pricing, bilingual task classification, multi-agent workflow planning, and adaptive fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yb98k999](https://clawhub.ai/user/yb98k999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure a PaleBlueDot AI TokenRouter provider, synchronize available models, inspect live pricing, and generate model-routing plans for coding, analysis, writing, creative, translation, and simple tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify OpenClaw model provider settings and allowed models.

Mitigation: Review the intended provider URL and model list before enabling or syncing, and keep a backup of the OpenClaw configuration.

Risk: The setup flow stores a TokenRouter API key locally and command-line usage can expose secrets in shell history.

Mitigation: Use only user-provided credentials, avoid pasting secrets into reusable command history where possible, and rotate the key if it may have been exposed.

Risk: Bundled local file-inspection utilities can read and print workspace files.

Mitigation: Remove, ignore, or restrict smart_find.py and smart_map.py unless local file inspection is explicitly needed.

## Reference(s):

- [Smart Model Router on ClawHub](https://clawhub.ai/yb98k999/skills/task-based-model-router)
- [PaleBlueDot AI](https://www.palebluedot.ai)
- [PaleBlueDot AI TokenRouter Pricing API](https://www.palebluedot.ai/openIntelligence/api/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands, configuration updates, and optional JSON execution plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw provider settings, model allow lists, routing preferences, swarm_plan.json, swarm_memory.json, and swarm_insights.json.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
