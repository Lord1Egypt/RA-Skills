## Description:

Complete Vrbo toolkit for search, availability, listing detail, price, cross-OTA price comparison, and reviews through StayingAPI's unified schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve lodging search, availability, listing, price, price-comparison, and review data for Vrbo-centered travel workflows. It is appropriate when broad StayingAPI coverage is useful and a focused Vrbo-only tool surface is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live STAYINGAPI_KEY could be exposed if stored in an unsafe profile, config file, or repository.

Mitigation: Use a protected secret store or narrowly scoped runtime environment, avoid committing keys, use sandbox keys for testing, and rotate any key that may have been exposed.

Risk: The skill contacts StayingAPI and can support non-Vrbo platforms despite the Vrbo-focused name.

Mitigation: Disclose external API use to operators and filter requests to Vrbo when the workflow must stay Vrbo-specific.

Risk: Availability, pricing, and comparison results may involve async jobs, partial results, or single-offer coverage.

Mitigation: Honor job status, Retry-After, warnings, and pagination metadata, and check offer counts before presenting a result as a multi-platform comparison.

## Reference(s):

- [StayingAPI Homepage](https://stayingapi.com)
- [StayingAPI Documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI Contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI API Key Setup](references/auth-setup.md)
- [ClawHub Skill Page](https://clawhub.ai/stayingapi/skills/vrbo-full)
- [Publisher Profile](https://clawhub.ai/user/stayingapi)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with endpoint descriptions, request parameters, headers, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com; sandbox keys return fixtures and live keys return real data.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
