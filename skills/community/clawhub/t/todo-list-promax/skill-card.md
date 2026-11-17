## Description:

Captures, organizes, and reminds users about personal to-dos from chat in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use it to capture personal tasks from chat, organize and review them by due date, priority, and tags, and receive opt-in daily reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had incomplete coverage, with one static check degraded and some references unresolved.

Mitigation: Review the skill and confirm its storage and reminder behavior in your environment before enabling it.

Risk: Task text and attachments are retained in workspace storage, including original source messages.

Mitigation: Use a private workspace, avoid recording sensitive details, and review or remove stored todo data when needed.

Risk: Daily reminders send task summaries into the user's chat.

Mitigation: Enable reminders only with the user's consent and use a private conversation; reminders omit original source messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z-zihan/skills/todo-list-promax)
- [Publisher profile](https://clawhub.ai/user/z-zihan)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Chat responses, Markdown task lists, JSON todo records, and optional reminder setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for capturing, querying, updating, and reminding on personal tasks]

## Skill Version(s):

2.2.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
