## Description:

End-to-end Toingg ops: create campaigns, optionally schedule daily analytics pulls, and turn Excel contact sheets into WhatsApp outreach via add_contacts and send_whatsapp_templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinavpgagi](https://clawhub.ai/user/abhinavpgagi)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Toingg campaign workflows, including campaign creation, campaign lookup, on-demand calls, analytics pulls, contact uploads, and WhatsApp template sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger outbound calls or WhatsApp template sends to contact lists.

Mitigation: Use it only with authorized Toingg accounts, confirm recipient opt-in, and verify applicable calling and messaging rules before bulk sends.

Risk: Contact exports, campaign payloads, analytics snapshots, and API responses can contain personal or business-sensitive data.

Mitigation: Store generated files in access-controlled locations, avoid committing sensitive outputs, and use short retention periods.

Risk: A broad Toingg API token could allow unintended campaign, contact, or messaging actions.

Mitigation: Use a limited Toingg token and confirm the token is available only in the environments that need to run the scripts.

## Reference(s):

- [Contact Upload + WhatsApp Template Workflow](references/contact-workflow.md)
- [Analytics Cron Playbook](references/analytics-cron.md)
- [Toingg Campaign Payload Template](references/payload-template.md)
- [ClawHub Skill Page](https://clawhub.ai/abhinavpgagi/skills/toingg-create-campaign)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON payloads, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON payloads, contact exports, analytics snapshots, and logged API responses when the agent runs the bundled scripts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
