## Description:

Search Redfin listings for sale, sold or for rent, pull one property in full with the Redfin Estimate and MLS fact sheet, and read housing-market stats for a region.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and real-estate analysts use this skill to search Redfin sale, sold, and rental listings, retrieve full property details, and gather regional housing-market statistics through Scavio's Redfin data API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends property search parameters and listing or region identifiers to Scavio's third-party API.

Mitigation: Use the skill only when Scavio is an acceptable third-party service for the workflow and avoid sending sensitive or unnecessary search context.

Risk: The required SCAVIO_API_KEY could be exposed if pasted into source files, logs, or shared transcripts.

Mitigation: Store SCAVIO_API_KEY in an environment variable or secret store and keep it out of committed code and user-visible output.

Risk: Optional SDK installation adds dependency exposure for users who only need direct API examples.

Mitigation: Use direct HTTPS examples or an isolated virtual environment when minimizing dependency risk is important.

## Reference(s):

- [Scavio Redfin Search Documentation](https://scavio.dev/docs/redfin-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/redfin-property-data)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API Calls, configuration]

**Output Format:** [Markdown with JSON request examples and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call Scavio's Redfin endpoints and return structured JSON-backed property and market data.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
