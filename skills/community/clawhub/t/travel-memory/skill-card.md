## Description:

Travel Memory stores trip plans, preferences, and past trips so agents can plan, rebook, and advise without re-asking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log itineraries, preferences, bookings, and post-trip lessons, then recall that travel memory when planning or rebooking future trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel plans, lodging details, preferences, and trip history can be sensitive when stored or recalled through the BlueColumn/Supabase API.

Mitigation: Store only details needed for future planning, avoid unnecessary identifiers or exact details, and review the provider's privacy, retention, and deletion practices before use.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/travel-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends travel memory fields to BlueColumn/Supabase-hosted endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
