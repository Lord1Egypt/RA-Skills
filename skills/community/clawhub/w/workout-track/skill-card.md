## Description:

Logs a strength training session and inserts it into the life_db database after parsing workout details from the user's message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn natural-language strength-training notes into confirmed records in their own PostgreSQL life_db sport schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles database credentials and user-derived workout text through a shell-based insert path.

Mitigation: Review the skill before installing, use a dedicated low-privilege database account, protect the .env file, and avoid sensitive health notes until a safer structured interface is available.

Risk: Confirmed inserts persist personal fitness or health-adjacent notes in the configured database.

Mitigation: Review the confirmation summary before approving an insert and limit notes to information appropriate for the database's access controls and retention policy.

## Reference(s):

- [Workout Track ClawHub page](https://clawhub.ai/spideystreet/skills/workout-track)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown and plain text summaries with JSON payloads and shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before insertion and writes confirmed sessions to the PostgreSQL sport schema.]

## Skill Version(s):

1.0.2 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
