## Description:

Use when the user asks about their sleep data, dream history, or wants to query sleep entries from the Soft Pillow app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kivs](https://clawhub.ai/user/kivs)

### License/Terms of Use:


## Use Case:

External Soft Pillow users use this skill to let an agent query their sleep status, sleep entries, dream history, notes, mood, disruptions, and related records from the Soft Pillow API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Soft Pillow sleep, dream, notes, mood, disruption, and related entry data when given an API key.

Mitigation: Install and use it only when that data access is acceptable, and avoid requesting entries that should not be processed by the agent or the Soft Pillow API.

Risk: Exposure of the Soft Pillow API key could allow unauthorized access to the user's account data.

Mitigation: Keep the API key private, store it locally, and revoke it from Soft Pillow app settings when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kivs/skills/soft-pillow)
- [Soft Pillow homepage](https://paevita.com/en/soft-pillow)
- [Soft Pillow App Store listing](https://apps.apple.com/us/app/soft-pillow/id6757248808)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Soft Pillow API key and may return personal sleep, dream, notes, mood, disruption, and activity-related entry data.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
