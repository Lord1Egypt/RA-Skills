## Description:

Fetches health data from the Withings API including weight, body composition, activity, and sleep for user-requested health tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hisxo](https://clawhub.ai/user/hisxo)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to authenticate to a Withings account and retrieve weight, body composition, daily activity, and sleep measurements for personal health tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Withings health data.

Mitigation: Use it only when the user intends to grant access to their Withings account and is comfortable managing that personal health data.

Risk: OAuth tokens are stored locally in plaintext.

Mitigation: Restrict local file permissions, exclude tokens.json from repositories and archives, and revoke Withings tokens if the token file is exposed.

Risk: Client secrets may be placed in a .env file that is not actually ignored by this package.

Mitigation: Keep .env out of source control and archives, prefer managed environment variables where available, and rotate Withings app credentials if exposed.

## Reference(s):

- [Withings Developer Portal](https://developer.withings.com/)
- [ClawHub skill page](https://clawhub.ai/hisxo/skills/withings-health)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and WITHINGS_CLIENT_ID/WITHINGS_CLIENT_SECRET; retrieves sensitive personal health data through the Withings API.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
