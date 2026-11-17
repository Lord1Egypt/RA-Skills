## Description:

Vehicle OS helps an agent track service history, maintenance schedules, mechanics, registration, insurance, administrative deadlines, and costs across cars, trucks, motorcycles, boats, RVs, and trailers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to maintain local records for owned vehicles, log services and costs, track mechanics, and surface maintenance or administrative due dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed vehicle, registration, insurance, or loan information may be retained in a local JSON file.

Mitigation: Store only necessary details, avoid full VINs, plate numbers, policy details, addresses, and loan information unless needed, and periodically review or delete saved records.

Risk: Built-in maintenance intervals may not match a specific vehicle, operating conditions, or manufacturer guidance.

Mitigation: Use the suggested schedules as adjustable defaults and confirm important maintenance decisions against the owner's manual or a qualified mechanic.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chris/skills/vehicle-os)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational Markdown responses with local JSON record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists vehicle records in vehicle-data.json when the host agent supports the skill data directory.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
