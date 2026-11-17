## Description:

Searches public Tesla job postings by role, department, or location and retrieves full posting details through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, recruiters, and researchers can search public Tesla openings and inspect the description and requirements of individual postings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to a third-party service.

Mitigation: Use only for public job-posting research and avoid sensitive search terms.

Risk: The Crawlora API key could be exposed if stored in code or shared.

Mitigation: Keep the key in CRAWLORA_API_KEY; do not hardcode or commit it.

## Reference(s):

- [Tesla Jobs endpoint reference](reference/endpoints.md)
- [Tesla Careers](https://www.tesla.com/careers)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown summaries of JSON job listings and posting details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listings are paginated and contain metadata only; full descriptions require a separate posting lookup.]

## Skill Version(s):

1.0.17 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
