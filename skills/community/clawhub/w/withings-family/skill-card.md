## Description:

Fetches health data from the Withings API for multiple family members including weight, body composition (fat, muscle, bone, water), activity, and sleep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

External users and their authorized family members use this skill to retrieve Withings health measurements, activity data, and sleep summaries through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves sensitive personal and family health records.

Mitigation: Use it only for accounts whose owners have explicitly authorized access, and avoid running it on shared or untrusted machines.

Risk: OAuth refresh tokens are stored persistently on the local machine.

Mitigation: Treat the local token directory as sensitive, keep token files private, delete tokens when access is no longer needed, and revoke Withings access if a device may be compromised.

Risk: Multiple family members can be configured, which can create consent and data-boundary confusion.

Mitigation: Authenticate each family member separately and use clear per-user identifiers so requests retrieve only the intended person's data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/withings-family)
- [Publisher profile](https://clawhub.ai/user/odrobnik)
- [Withings Developer Portal](https://developer.withings.com/)
- [Withings OAuth authorization endpoint](https://account.withings.com/oauth2_user/authorize2)
- [Withings OAuth token endpoint](https://wbsapi.withings.net/v2/oauth2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Withings API credentials, and local per-user OAuth token files.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
