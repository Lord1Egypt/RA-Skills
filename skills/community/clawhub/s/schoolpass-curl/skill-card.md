## Description:

Read a SchoolPass parent account directly with curl against the regional SchoolPass REST API (a busapi shard on school-pass.net), without running the MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

SchoolPass parents can use the skill for one-off terminal access to their students, arrival and dismissal calendars, pickup changes, drivers, dismissal locations, and school information. The request recipes also show how to submit or cancel arrival and dismissal changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Although the skill is described as read-oriented, its request examples include commands that create or delete student arrival and dismissal changes.

Mitigation: Review each POST or DELETE request before running it, confirm the student, date, and change type, and reread the calendar to verify the result.

Risk: The login recipe may select an unintended account identity.

Mitigation: Confirm the selected Parent identity and school code are for the intended account before making authenticated requests.

Risk: Credentials, bearer tokens, and student or family information may be exposed through terminal output or shared transcripts.

Mitigation: Keep credentials in environment variables, avoid printing or sharing passwords and bearer tokens, and limit output to information needed for the task.

## Reference(s):

- [Ready-to-run requests](artifact/references/requests.md)
- [ClawHub skill listing](https://clawhub.ai/chrischall/skills/schoolpass-curl)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides curl request examples and JSON request bodies; API responses are JSON.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
