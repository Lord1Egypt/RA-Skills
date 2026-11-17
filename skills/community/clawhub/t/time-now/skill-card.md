## Description:

Get the current local time, UTC offset, DST status, and timezone metadata for any IANA timezone or public IP address using the free Time.Now API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisyau83](https://clawhub.ai/user/chrisyau83)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask for current time and timezone details by IANA timezone or public IP. The skill also supports checking available timezones and API health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP-based lookups send the queried public IP to Time.Now, and automatic lookup reflects the agent host rather than necessarily the user's location.

Mitigation: When privacy or location accuracy matters, use a user-provided timezone or city and explain that automatic IP lookup reflects the agent host.

## Reference(s):

- [Time.Now developer documentation](https://time.now/developer)
- [Time.Now OpenClaw skill documentation](https://time.now/developer/openclaw)
- [ClawHub skill page](https://clawhub.ai/chrisyau83/skills/time-now)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Natural-language time and timezone information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned timezone, local time, UTC offset, and daylight-saving status when relevant.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
