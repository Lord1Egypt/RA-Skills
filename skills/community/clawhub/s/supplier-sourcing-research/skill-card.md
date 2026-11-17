## Description:

Discover and compare potential suppliers using ImportYeti shipment reports and public business websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Sourcing teams and business researchers use this skill to shortlist suppliers, compare observed trade relationships and product fit, and identify questions for supplier qualification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier queries, public URLs, and an API key are sent to Crawlora's API; sensitive business details could be disclosed.

Mitigation: Keep the key in an environment variable and avoid confidential business data unless Crawlora is approved for it.

Risk: Shipment records may be incomplete or misread as proof of a supplier's capabilities.

Mitigation: Review API output, preserve source links and coverage windows, and verify capabilities directly before qualification.

## Reference(s):

- [Supplier Sourcing Research on ClawHub](https://clawhub.ai/crawlora-org/skills/supplier-sourcing-research)
- [Endpoint reference](reference/endpoints.md)
- [ImportYeti data coverage](https://www.importyeti.com/our-data)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown supplier shortlist with cited evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes shipment date and metric scope, product fit, source links, and open qualification questions.]

## Skill Version(s):

1.0.13 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
