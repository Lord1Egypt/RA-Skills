## Description:

Extracts important family-related information from recent mobile phone notifications, groups it by family member, and marks whether each item needs action or is informational.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

People use this skill to review family-related notifications for a requested date range and quickly see important updates from spouses, parents, elders, children, teachers, and schools. It helps distinguish action-needed items from messages that are only useful to know while filtering chat, marketing, bills, travel, and unrelated notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive local phone notification history, including family, school, chat, SMS, email, and other app notifications, before filtering.

Mitigation: Invoke it only for explicit family-summary requests, use narrow date ranges, and install it only when this notification access is acceptable.

Risk: Broad trigger phrases may cause the skill to inspect notification history more often than users expect.

Mitigation: Use specific prompts that name the family-summary task and the intended date range.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-family-digest-en)
- [ClawHub publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style summary text with grouped family sections and action markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local notification-history files for requested dates and returns session text only; it does not write files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
