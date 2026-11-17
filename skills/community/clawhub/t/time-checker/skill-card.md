## Description:

Check accurate current time, date, and timezone information for any location worldwide using time.is.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer current-time, date, and timezone questions for cities or countries worldwide, especially when scheduling across time zones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script that calls curl and sends the requested location name to time.is.

Mitigation: Install and run it only when sharing the queried location with time.is is acceptable.

Risk: The artifact includes a persona instruction unrelated to neutral time reporting.

Mitigation: Remove or ignore the persona instruction when neutral responses are required.

## Reference(s):

- [time.is](https://time.is)
- [ClawHub skill page](https://clawhub.ai/1999azzar/skills/time-checker)
- [Publisher profile](https://clawhub.ai/user/1999azzar)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include location, current time, timezone details, and the source URL returned by time.is.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
