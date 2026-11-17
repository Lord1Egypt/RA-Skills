## Description:

Read normalized Vrbo reviews for a listing, with native rating scales preserved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Vrbo guest reviews and ratings for a known listing, using StayingAPI while preserving each platform's native rating scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Listing identifiers or URLs are sent to StayingAPI when fetching reviews.

Mitigation: Install only when this data sharing is acceptable; use a sandbox stay_test_ key for evaluation before live use.

Risk: The required STAYINGAPI_KEY could be exposed through commits, logs, or pasted chat content.

Mitigation: Store live keys in a secure secret manager or protected environment variable and avoid committing, logging, or sharing them.

Risk: Review ratings may be misleading if native rating scales are silently rescaled or omitted.

Mitigation: Preserve and display each rating's native scale when summarizing or comparing reviews.

## Reference(s):

- [StayingAPI authentication setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details and optional shell commands; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a STAYINGAPI_KEY and internet access to api.stayingapi.com; pagination and async job polling may apply.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
