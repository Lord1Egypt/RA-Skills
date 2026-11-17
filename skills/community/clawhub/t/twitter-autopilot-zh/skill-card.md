## Description:

Searches Twitter/X data, monitors account activity and trends, and uses the AISA relay to post and perform account interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to read Twitter/X profile, timeline, search, trend, follower, and mention data, then publish posts or perform likes, follows, and related interactions after OAuth authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live Twitter/X posting and account interaction actions.

Mitigation: Require clear user confirmation before post, like, follow, or unfollow actions and test with non-production accounts before real use.

Risk: Normal status and posting outputs can expose AISA_API_KEY.

Mitigation: Avoid using real keys with status or posting commands until outputs redact secrets; rotate any key exposed in logs or transcripts.

Risk: Relay requests depend on trusting the AISA relay destination.

Mitigation: Use only trusted HTTPS relay hosts and do not override the relay base URL to untrusted destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/twitter-autopilot-zh)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON CLI outputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate live Twitter/X posting, like, follow, or unfollow actions through the AISA OAuth relay.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
