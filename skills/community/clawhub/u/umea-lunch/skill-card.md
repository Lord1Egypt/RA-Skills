## Description:

Gets today's lunch menus from restaurants in Umeå by fetching live data from umealunchguide.se.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simskii](https://clawhub.ai/user/simskii)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve current or date-specific Umeå restaurant lunch menus, filter by restaurant, and present dishes, prices, dietary tags, and location details.

### Deployment Geography for Use:

Global; menu coverage is specific to Umeå, Sweden.

## Known Risks and Mitigations:

Risk: The skill makes a live request to umealunchguide.se when asked for lunch data, so availability and returned menu content depend on that external public site.

Mitigation: Use the skill when live Umeå lunch data is needed, and treat unavailable or malformed responses as an external data-source failure rather than an agent decision.

## Reference(s):

- [Umeå Lunch Guide](https://umealunchguide.se/)
- [ClawHub Skill Page](https://clawhub.ai/simskii/skills/umea-lunch)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON from the helper script, typically summarized as Markdown or plain text by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional date, restaurant-name filter, and restaurant listing parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
