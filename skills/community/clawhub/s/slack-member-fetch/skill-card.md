## Description:

Fetch Slack workspace or channel member information through the Slack Web API and return structured member records for downstream automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donigwapo](https://clawhub.ai/user/donigwapo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, workspace administrators, and automation agents use this skill to list Slack workspace members or channel-specific members for directory review, reporting, or machine-readable exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slack member exports can contain sensitive employee directory data such as email addresses, titles, admin or owner status, and channel membership.

Mitigation: Use only authorized Slack bot tokens, store exports in approved locations, and avoid committing or sharing exported files.

## Reference(s):

- [Setup and usage](references/setup-and-usage.md)
- [Slack Web API](https://slack.com/api)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON printed to stdout or written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Slack user IDs, names, display names, emails when scoped, titles, time zones, admin/owner flags, bot status, and deletion status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
