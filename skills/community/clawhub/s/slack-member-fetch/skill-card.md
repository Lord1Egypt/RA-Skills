## Description: <br>
Fetches Slack member information from a workspace or a specific Slack channel using the Slack Web API for member lists, profile lookups, channel membership exports, and downstream automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donigwapo](https://clawhub.ai/user/donigwapo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to fetch Slack workspace or channel member records as structured JSON for audits, roster exports, and downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack member exports can contain personal and role-related employee information. <br>
Mitigation: Run the skill only with authorization, store output as sensitive data, and share exports only with approved recipients. <br>
Risk: A broad Slack bot token or email scope can expose more data than needed. <br>
Mitigation: Use the least-privileged Slack app possible and grant users:read.email only when email addresses are required. <br>
Risk: The Slack bot token grants API access if exposed. <br>
Mitigation: Keep SLACK_BOT_TOKEN in a protected environment variable or secret store, and rotate the token if it is disclosed. <br>


## Reference(s): <br>
- [Setup and usage](references/setup-and-usage.md) <br>
- [Slack Web API](https://slack.com/api) <br>
- [ClawHub skill page](https://clawhub.ai/donigwapo/slack-member-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script output is structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write JSON output to a user-specified file; output may include Slack profile fields such as email, title, timezone, and role flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
