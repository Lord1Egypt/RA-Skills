## Description:

Monitor one or more Twitter/X usernames via the 6551 API, generate a short humorous reply with `openclaw agent --json`, and submit the reply through an already logged-in Chrome X session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yugulugulu](https://clawhub.ai/user/yugulugulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local workflow that watches configured Twitter/X usernames, generates brief replies, posts them through a logged-in Chrome session, and sends status notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically post public X replies from a logged-in browser session using model-generated content.

Mitigation: Use only accounts approved for this automation, add manual approval or dry-run behavior before posting, and review generated replies before enabling unattended operation.

Risk: The workflow depends on an authenticated browser session and a Twitter API token.

Mitigation: Use a dedicated Chrome profile with no unrelated logged-in sessions and protect the TWITTER_TOKEN environment variable.

Risk: Tweet activity and posting status may be sensitive if routed to notification channels.

Mitigation: Limit notification destinations to approved recipients and disable or restrict notifications when monitored activity is sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yugulugulu/skills/twitter-listen-comment)
- [Config](references/config.md)
- [Example configuration](references/config.example.json)
- [6551 Twitter search API endpoint](https://ai.6551.io/open/twitter_search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local automation behavior that writes state and log files and may submit public X replies when executed.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
