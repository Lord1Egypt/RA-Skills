## Description:

Read a SchoolPass parent account with curl against its regional REST API for one-off checks of students, calendars, pickup changes, drivers, dismissal locations, and school information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents use this skill for one-off terminal checks of SchoolPass account details and calendars, and can submit or cancel arrival or dismissal changes when explicitly authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented commands can submit or cancel arrival and dismissal changes that affect a child's school arrangements.

Mitigation: Use reads for account checks; run changes only in an explicitly authorized workflow after confirming the child, date, intended action, and API host through the school portal.

Risk: Login credentials and bearer tokens provide access to sensitive parent and student information.

Mitigation: Protect credentials, keep tokens out of shared transcripts, and follow the documented single-attempt login guidance.

Risk: The request examples refer to a live-check script that is absent from the release artifacts.

Mitigation: Inspect the script from a trusted source before running it.

## Reference(s):

- [Ready-to-run requests](references/requests.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON]

**Output Format:** [Markdown with inline bash and jq code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the user's SchoolPass credentials, school code, and regional API host.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
