## Description:

Response Timing helps an agent decide whether to reply or remain silent when a user may or may not be addressing the current agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebly](https://clawhub.ai/user/ebly)

### License/Terms of Use:


## Use Case:

Agent builders and workspace users use this skill to control group-chat behavior, especially in Feishu-style conversations, so the agent responds only when addressed, assigned, or clearly useful. It is intended to reduce unwanted interjections while preserving responses for direct mentions, relevant follow-ups, urgent requests, and clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad emergency-response guidance could cause the agent to interject in sensitive or crowded group chats without being directly addressed.

Mitigation: Tighten emergency and follow-up rules for those environments so the agent defaults to NO_REPLY unless directly mentioned, clearly assigned, or clearly able to help.

Risk: Ambiguous names, aliases, or role boundaries could cause replies intended for another person or agent.

Mitigation: Keep agent names, aliases, and responsibility boundaries explicit, and prefer a brief clarification only when the message plausibly addresses this agent.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; may lead the agent to produce NO_REPLY when it should stay silent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
