## Description:

Helps agents manage ReachOwl social listening, outreach campaigns, content scheduling, lead imports, and CRM follow-ups across Facebook, Instagram, and WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jahanzaibbotsify](https://clawhub.ai/user/jahanzaibbotsify)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to monitor social discussions, prepare and manage outreach and posts, and organize leads and follow-ups through connected ReachOwl accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social outreach and scheduled automations may send unwanted messages or posts at scale.

Mitigation: Confirm the audience, message text, limits, and schedule; start campaigns paused and obtain approval before activation.

Risk: Lead collection and CRM imports may involve personal contact data and unsolicited outreach.

Mitigation: Use permitted public sources, confirm consent and opt-outs, and follow applicable platform rules and anti-spam requirements.

Risk: Webhooks may send contact or campaign data to an unintended destination.

Mitigation: Verify each destination URL and event selection with the user before enabling a webhook.

Risk: Account access or destructive changes may affect connected social accounts and CRM records.

Mitigation: Prefer token authentication over passwords and require explicit confirmation before deletions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jahanzaibbotsify/skills/reachowl-skills)
- [ReachOwl website](https://reachowl.com)
- [ReachOwl MCP server](https://reachowl.com/mcp)
- [ReachOwl setup guide](https://github.com/SaaSBakers/reachowl-skills#setup)
- [ReachOwl Lead Finder on Apify](https://apify.com/superior_couch/reachowl-lead-finder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown with suggested messages, summaries, and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ReachOwl account and connected social accounts for supported actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and primary skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
