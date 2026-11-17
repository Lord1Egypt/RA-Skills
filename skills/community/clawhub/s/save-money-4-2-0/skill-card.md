## Description:

Auto-detects task complexity for Claude models, keeping simple work on Haiku and routing complex work to Sonnet to reduce API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

External users and developers can use this behavioral skill to route Claude interactions between cheaper and stronger models based on task complexity while keeping simple responses concise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full task prompts may be forwarded automatically to Sonnet, including potentially sensitive work.

Mitigation: Review before installation and require explicit user confirmation before escalation in sensitive contexts.

Risk: Model switches may be undisclosed unless the user asks.

Mitigation: Configure the skill or operating policy to disclose routing decisions when escalation occurs.

Risk: Broad routing rules may escalate more prompts than expected.

Mitigation: Tune escalation triggers and monitor model usage after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sieyer/skills/save-money-4-2-0)
- [Publisher profile](https://clawhub.ai/user/sieyer)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce concise direct responses for simple tasks or routing guidance for complex tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 4.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
