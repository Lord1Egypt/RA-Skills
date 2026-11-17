## Description:

Native Telegram To-Do checklists: create, append, toggle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bablobanov](https://clawhub.ai/user/bablobanov)

### License/Terms of Use:

MIT-0

## Use Case:

Telegram users and assistants create and maintain native checklists in Saved Messages or explicitly permitted groups and topics, including lists assembled from verified chat messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Telethon user session can access and change checklist data in its permitted destinations.

Mitigation: Protect the session file and keep TELETHON_CHECKLIST_CHATS narrowly scoped to intended chats and topics.

Risk: Checklist items may expose sensitive information or carry untrusted instructions from chats.

Mitigation: Exclude secrets and personal data; treat chat contents as data, verify sources, and act only on an explicit user request.

Risk: A checklist could be shared or sent to an unintended permitted chat or topic.

Mitigation: Review the target and offline plan or dry run before creating; enable shared completion only when explicitly requested.

## Reference(s):

- [Telegram Checklist on ClawHub](https://clawhub.ai/bablobanov/skills/telegram-checklist)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON results and concise text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates native Telegram checklists; results include verified state and warnings when available.]

## Skill Version(s):

1.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
