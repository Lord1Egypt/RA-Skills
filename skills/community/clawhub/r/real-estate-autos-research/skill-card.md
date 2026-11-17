## Description:

Helps agents research home listings, property estimates and market trends, and used-car listings through Crawlora's property and vehicle data endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare home listings, property estimates and regional trends, or search used cars and inspect vehicle and dealer details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search inputs, including addresses, ZIP codes, listing URLs and property or vehicle IDs, are sent to Crawlora and potentially upstream listing sources.

Mitigation: Confirm the user is comfortable sharing those inputs before making requests; avoid submitting unnecessary sensitive information.

Risk: Rightmove routes are available in the endpoint reference and helper but not disclosed in the skill's main description.

Mitigation: Disclose Rightmove use clearly to users; the publisher should update the description or remove unintended routes.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/real-estate-autos-research)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON data with human-readable research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be paginated; property values and listings are not professional advice.]

## Skill Version(s):

1.0.21 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
