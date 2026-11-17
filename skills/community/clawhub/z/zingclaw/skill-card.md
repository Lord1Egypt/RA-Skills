## Description:

Calls the ZingAPI creative-list interface to search ad creatives and materials by industry, country or region, channel, keyword, creative type, AI tags, time range, and sorting criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zingfront-ad](https://clawhub.ai/user/zingfront-ad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert natural-language ad creative search requests into signed ZingAPI creative-list calls and receive concise creative summaries or raw API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires ZingAPI credentials to sign production API requests.

Mitigation: Store ZINGAPI credentials in protected environment variables or a secret manager, avoid passing secrets on the command line, and never include secret values in replies, logs, errors, or shared dry-run output.

Risk: Raw request bodies can send broad or unintended ad creative queries to the ZingAPI service.

Mitigation: Review generated JSON request bodies before sending them, especially when using full-control body mode instead of the script's typed parameters.

## Reference(s):

- [ZingAPI creative-list endpoint](https://openapi.dataideaglobal.com/zingapi/v1/creative/list/{customer_name})
- [Parameter reference](references/parameters.md)
- [Input mapping](references/input-mapping.md)
- [Response fields](references/response-fields.md)
- [Usage examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown summaries with inline shell commands and optional raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output groups ad creative results by advertiser, material, placement, metrics, copy, links, game tags, AI material tags, and key raw fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
