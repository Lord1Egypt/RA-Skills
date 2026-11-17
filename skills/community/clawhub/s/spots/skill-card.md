## Description:

Exhaustive Google Places search using grid-based scanning. Finds ALL places, not just what Google surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foeken](https://clawhub.ai/user/foeken)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run or guide exhaustive Google Places searches for venues in a named area or around coordinates, filter results by rating, review count, and open status, retrieve reviews, and export results as JSON, CSV, or a map.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users to install or use a mutable external spots executable.

Mitigation: Use a pinned, reviewed version of the spots binary before installation or execution.

Risk: The skill references a Google API key and an exact 1Password secret location.

Mitigation: Restrict the Google API key to the needed APIs and quotas, and keep the secret out of agent transcripts, logs, and scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foeken/skills/spots)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of the external spots binary and Google Places API credentials; supported result exports include JSON, CSV, and map output.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
