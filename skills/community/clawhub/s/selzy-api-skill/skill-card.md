## Description:

Creates and sends Selzy email marketing campaigns, manages contacts, templates, segments, scheduling, A/B tests, and campaign performance analysis through the Selzy API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selzy-openclaw](https://clawhub.ai/user/selzy-openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, developers, and operators use this skill to prepare and manage Selzy email campaigns from chat while checking recipient lists, sender verification, scheduling, and campaign metrics before API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaigns can be sent or scheduled to the wrong audience if list_id, list name, recipient count, sender, subject, body, send time, or timezone are not verified immediately before campaign creation.

Mitigation: Call getLists or getList first, require createEmailMessage to include list_id, compare recipient count against user expectations, and require fresh explicit confirmation before createCampaign.

Risk: Rapid or automated campaign creation can trigger Selzy fraud controls or account blocking.

Mitigation: Enforce a maximum of one createCampaign call per hour, avoid batch campaign creation, and stop immediately if API responses suggest account review or blocked campaigns.

Risk: API keys and contact data may appear in GET request URLs or logs.

Mitigation: Use a restricted Selzy API key when available, keep SELZY_API_KEY in environment configuration, and do not display or log full API URLs containing credentials or personal data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/selzy-openclaw/skills/selzy-api-skill)
- [Selzy API Documentation](https://selzy.com/en/support/api/)
- [Selzy API Limits](https://selzy.com/en/support/api/common/selzy-api-limits/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SELZY_API_KEY; campaign workflows require list, recipient count, sender, timing, and confirmation checks before campaign creation.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact metadata reports 2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
