## Description:

List and search WhatsApp Business labels/tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to inspect local WhatsApp Business label data, list available labels, and find contacts or chats associated with a selected label.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local WhatsApp Business cache data, which can include contact names, account identifiers, and label relationships.

Mitigation: Install and run it only in environments where the agent is allowed to access that local WhatsApp Business cache.

Risk: Command output may expose contact or chat metadata from local cache files.

Mitigation: Review outputs before sharing them outside the trusted workspace or adding them to logs, tickets, or reports.

## Reference(s):

- [WhatsApp Labels skill page](https://clawhub.ai/marcosrippel/skills/whatsapp-labels)
- [Publisher profile](https://clawhub.ai/user/marcosrippel)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands read local WhatsApp Business cache files and return label or contact records as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
