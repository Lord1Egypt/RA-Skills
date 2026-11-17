## Description:

Converts natural-language day and relative-date references into the soonest future calendar date in ISO format for scheduling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtheodas](https://clawhub.ai/user/jtheodas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before creating calendar events, proposing meeting times, or communicating specific dates derived from phrases such as "next Friday", "this Wed", or "tomorrow".

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone-sensitive scheduling can be wrong because the helper accepts a timezone parameter but the reviewed implementation does not apply it.

Mitigation: Verify the resolved date against the intended timezone before creating real calendar events or sending confirmed dates to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jtheodas/skills/relative-date-resolver)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [ISO date string with Markdown usage guidance and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns YYYY-MM-DD for the resolved future date; invalid or ambiguous expressions may raise an error or use the most reasonable future match.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
