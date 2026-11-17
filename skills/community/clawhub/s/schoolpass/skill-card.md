## Description:

Helps parents review a child’s SchoolPass arrival and dismissal details and request schedule changes with confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents use the skill to review linked students’ arrival and dismissal schedules, pickup changes, authorized drivers, locations, and school information. They can also submit or cancel a schedule change after reviewing and confirming the specific change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a parent account containing students’ schedules and pickup details, and requires account credentials.

Mitigation: Use a reviewed, pinned package version and protect the configuration containing the password. Never echo the password or a session token.

Risk: Submitting or canceling a dismissal change affects a child’s real arrival or pickup plan.

Mitigation: Keep confirmation set to ask-user, or refuse if only reads are needed. Review the child, date, and proposed change before approval; if submission status is uncertain, reread the calendar and do not resubmit.

## Reference(s):

- [Schoolpass on ClawHub](https://clawhub.ai/chrischall/skills/schoolpass)
- [schoolpass-mcp package](https://www.npmjs.com/package/schoolpass-mcp)
- [Project repository (linked in the skill)](https://github.com/chrischall/schoolpass-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language responses based on SchoolPass account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize schedules and pickup details; schedule changes require explicit confirmation.]

## Skill Version(s):

1.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
