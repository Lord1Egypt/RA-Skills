## Description:

Searches Singapore property rental and sale listings with filters for listing type, property type, bedrooms, bathrooms, price, size, MRT proximity, availability, and optional commute time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5kbpers](https://clawhub.ai/user/5kbpers)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Singapore rental or sale listings, compare listing details against user-provided filters, and optionally add commute estimates when a Google Maps API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commute calculations send the destination address and scraped property addresses to Google Routes API.

Mitigation: Use --commute-to only when address sharing with Google is acceptable, or omit the option to scrape listings without commute lookup.

Risk: Python dependencies are documented without pinned versions.

Mitigation: Install the scraper in a virtual environment and pin dependency versions before operational deployment.

Risk: --no-validate and --raw-param can bypass the documented parameter guardrails.

Mitigation: Keep validation enabled for normal use and reserve raw parameters for intentional testing of unsupported PropertyGuru query parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5kbpers/skills/sg-property-scraper)
- [PropertyGuru Parameter Reference](references/params.md)
- [PropertyGuru Singapore](https://www.propertyguru.com.sg)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration]

**Output Format:** [JSON array or plain text from the scraper CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include listing details, links, and optional driving and transit commute estimates when GOOGLE_MAPS_API_KEY is set.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
