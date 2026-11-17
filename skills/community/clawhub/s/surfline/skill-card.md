## Description:

Get surf forecasts and current conditions from Surfline public endpoints with no login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelcarranza](https://clawhub.ai/user/miguelcarranza)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Surfline spot IDs, fetch current conditions and short-range forecasts for specific spots, and summarize saved favorite surf spots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searched or saved Surfline spot IDs can reveal surf-location interests through outbound public-service requests and local files.

Mitigation: Use only spot IDs the user is comfortable querying, and review or delete ~/.config/surfline/favorites.json and ~/.cache/surfline when local surf-location history should not be retained.

Risk: Surfline public endpoint fields may change, causing missing, stale, or incomplete report content.

Mitigation: Inspect JSON output when summaries look wrong, keep request caching modest, and update the Surfline client parsing when endpoint payloads change.

## Reference(s):

- [ClawHub Surfline skill page](https://clawhub.ai/miguelcarranza/skills/surfline)
- [Surfline public services endpoint](https://services.surfline.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include raw Surfline forecast payloads; local favorites and cached forecast JSON are stored under the user's home directory.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
