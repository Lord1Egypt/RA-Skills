## Description:

Researches restaurant reviews, reservations, delivery menus, and grocery listings through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents researching restaurants, delivery options, or groceries use this skill to compare public reviews, menus, and store listings near a location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant or grocery searches can send an address, postal code, or coordinates to Crawlora.

Mitigation: Use coarse locations when exact delivery availability is unnecessary.

Risk: API requests use a Crawlora key; unrelated credentials or payment details should not be shared.

Mitigation: Keep the API key in CRAWLORA_API_KEY and limit requests to public listing, menu, and review data.

## Reference(s):

- [Supported endpoints and parameters](reference/endpoints.md)
- [Crawlora API and account information](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON data, Text guidance, Shell commands]

**Output Format:** [JSON API results with optional Markdown summaries and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on location and available public listings; this skill does not place orders or process payments.]

## Skill Version(s):

1.0.22 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
