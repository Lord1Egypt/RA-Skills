## Description:

Search Zillow listings for sale, for rent or sold, pull one property in full with Zestimate and tax history, and read a real-estate agent's profile and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Zillow sale, rental, and sold listings, retrieve full property records, and inspect real-estate agent profiles and reviews through Scavio's API. It supports property search, market monitoring, comparable analysis, and rent-versus-buy analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property and agent queries are sent to Scavio's API service and require a bearer API key.

Mitigation: Use a revocable SCAVIO_API_KEY with spending limits where possible, keep it out of source control, and prefer direct HTTPS examples if third-party SDK installation is not desired.

Risk: Zillow filter behavior can produce misleading results when a bare ZIP is combined with filters or when unsupported days_on_zillow values are used.

Mitigation: Use city names when applying filters or sorts, keep days_on_zillow to documented values, and treat zero-result responses as real filtered results instead of retrying unchanged.

Risk: Zestimate, rent estimates, listing details, and agent reviews can be mistaken for appraisals, purchase prices, or property reviews.

Mitigation: Label Zestimate and rent Zestimate values as estimates, never present agent reviews as reviews of a home, and do not fabricate addresses, prices, zpids, names, or review text.

Risk: Public listing data can still be misused to profile occupants of a home.

Mitigation: Use the data for property and market analysis only, and avoid occupant profiling or conclusions not supported by returned API fields.

## Reference(s):

- [Scavio Zillow Search API Documentation](https://scavio.dev/docs/zillow-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zillow-property-data)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=zillow-property-data)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/zillow-property-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response descriptions and Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to call Scavio HTTPS endpoints that return structured JSON envelopes for listing search, property detail, and agent review data.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
