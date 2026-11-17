## Description:

Remember Birthdays helps an agent store and recall birthdays, anniversaries, and special dates for timely greetings through BlueColumn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to save personal dates, recall upcoming birthdays and anniversaries, and draft timely greetings after confirming details with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends and persists names, special dates, relationship context, privacy preferences, and greeting history to BlueColumn's remote service.

Mitigation: Confirm each record with the user before storing it, avoid sensitive context unless necessary, and review BlueColumn retention, deletion, access-control, and API-key handling practices before use.

Risk: Stored relationship details can affect future greeting workflows if they are inaccurate, outdated, or duplicated.

Mitigation: Verify names and dates before drafting greetings, and store a short completion note after sending a greeting to reduce duplicate messages.

## Reference(s):

- [BlueColumn API Documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, text]

**Output Format:** [Markdown guidance with bash/curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends personal date records to BlueColumn endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
