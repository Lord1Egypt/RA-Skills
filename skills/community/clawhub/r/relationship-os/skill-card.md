## Description: <br>
Relationship OS enables AI agents to maintain relationship memory through event capture, open threads, exclusive memories, agent stances, and relationship growth stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhab03](https://clawhub.ai/user/chenhab03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users install this skill to give an agent persistent relationship context, local event memory, pending follow-up threads, shared memories, stance tracking, and stage-based interaction behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses sensitive emotional and relationship history in local .relationship files. <br>
Mitigation: Review the stored .relationship data, limit access to the workspace, and remove records that should not persist. <br>
Risk: Heartbeat and cron workflows can enable proactive outreach, including Telegram delivery. <br>
Mitigation: Enable scheduled delivery only when intentional, review pending threads before sending, and disable or tightly scope heartbeat delivery in sensitive environments. <br>
Risk: Debug logging and optional image generation can expose personal context or rely on ambient API credentials. <br>
Mitigation: Reduce verbose debug logging, protect generated logs, and review any image-generation setup and API key handling before use. <br>
Risk: The README includes advice about working around moderation boundaries for roleplay. <br>
Mitigation: Do not use moderation-workaround guidance; keep agent behavior within the model provider's safety policies and the deployment environment's requirements. <br>


## Reference(s): <br>
- [Event Memory Format Specification](references/event-schema.md) <br>
- [Relationship Stage Behavior Matrix](references/stage-matrix.md) <br>
- [Proactive Trigger Rules](references/motivation-rules.md) <br>
- [Selfie Module Rules](references/selfie-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON relationship state files, shell commands for scheduled follow-ups, and text guidance for agent behavior.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local .relationship state, can inject bootstrap context, and can trigger proactive follow-up workflows when enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, _meta.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
