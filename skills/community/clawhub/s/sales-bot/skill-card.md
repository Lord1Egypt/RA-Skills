## Description:

Automate lead capture and tracking with Supabase storage and Make.com email workflows, managing conversations from new to qualified status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-roman123](https://clawhub.ai/user/big-roman123)

### License/Terms of Use:

MIT

## Use Case:

Sales and support agents use this skill to capture lead contact details, trigger automatic email follow-up, track lifecycle status, and retrieve or update conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a powerful Supabase service-role key while handling sensitive lead and conversation data.

Mitigation: Use a narrowly scoped Supabase credential or backend RPC/API instead of a broad service-role key, and keep credentials in managed secret storage.

Risk: Tenant-scoping gaps around CRM data could expose or modify records across organizations.

Mitigation: Confirm organization filters and Supabase row-level security policies protect every read, update, and delete path before deployment.

Risk: Lead capture and automated email replies may collect contact details or send outreach before consent is established.

Mitigation: Add explicit consent checks before storing contact details or sending auto-replies, and define retention and redaction rules for conversation logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/big-roman123/skills/sales-bot)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Lead Schema](artifact/schemas/lead.json)
- [Conversation Schema](artifact/schemas/conversation.json)

## Skill Output:

**Output Type(s):** [JSON, text, configuration]

**Output Format:** [Structured JSON action results with short status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Supabase URL, Supabase service-role key, organization ID, and optional default priority.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, skill.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
