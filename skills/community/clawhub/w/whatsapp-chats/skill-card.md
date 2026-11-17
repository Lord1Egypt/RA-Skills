## Description:

List, search, and analyze WhatsApp conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to list, search, and summarize locally cached WhatsApp/Baileys chats, including contacts, groups, and basic chat counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal private contacts, phone numbers, group identifiers, and local WhatsApp/Baileys cache paths.

Mitigation: Run it only in workspaces where that disclosure is acceptable, and treat command output as sensitive.

Risk: Search and statistics results may be copied into broader agent context or user-visible responses.

Mitigation: Review and redact identifiers, names, phone numbers, group IDs, and local paths before sharing output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON from the helper script, with Markdown command examples in skill guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local WhatsApp/Baileys state and returns contact, group, search, or statistics data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
