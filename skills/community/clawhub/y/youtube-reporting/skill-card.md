## Description:

Helps agents manage YouTube Reporting jobs and retrieve bulk channel or playlist analytics reports through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Channel owners and analysts use this skill to list report types, schedule and manage reporting jobs, and download daily CSV reports. With separate approval, developers can automate an authorized reporting action using a hosted function and trigger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account grants Maton access to authorized YouTube Reporting data.

Mitigation: Connect only a trusted account and review the requested OAuth permissions before approving the connection.

Risk: Creating or deleting reporting jobs, or enabling hosted functions and triggers, can change reporting or run actions unattended.

Mitigation: Require explicit approval for each write or automation step, including the function, trigger, and destination.

Risk: Exposing a Maton API key or sending it to a report download host can disclose account access.

Mitigation: Prefer OAuth via the CLI; when an API key is necessary, keep it private and route downloads through Maton rather than sending the key to Google.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/byungkyu/skills/youtube-reporting)
- [Maton homepage](https://maton.ai)
- [YouTube Reporting API reference](https://developers.google.com/youtube/reporting/v1/reference/rest)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, CSV reports]

**Output Format:** [Markdown guidance and commands; downloaded CSV reports when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and an authorized YouTube Reporting connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
