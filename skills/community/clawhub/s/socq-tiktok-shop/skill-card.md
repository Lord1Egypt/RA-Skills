## Description:

Helps agents collect and analyze public TikTok Shop products, shops, creators, and sales signals through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to find and compare public TikTok Shop products, reviews, stores, and creator showcases, while tracking collection status and costs.

### Deployment Geography for Use:

Global; product and user-showcase endpoints currently support US only.

## Known Risks and Mitigations:

Risk: Research requests use a SocQ API key and send queries to the hosted SocQ service.

Mitigation: Confirm service use before installation, keep the key in the environment, and do not expose it in prompts or URLs.

Risk: Large or repeated collections can consume paid credits.

Mitigation: Check live pricing and credit limits, use a pinned or preinstalled CLI where possible, and confirm broad or paid collection runs before submitting.

Risk: Incomplete pagination or provider failures can yield misleading coverage.

Mitigation: Report pages read, failed requests, unsupported filters, and any remaining data; do not claim completeness when collection ends early.

## Reference(s):

- [SocQ TikTok Shop API documentation](https://docs.socq.ai/api-manual/tiktok-shop)
- [SocQ integrations overview](https://docs.socq.ai/integrations/overview)
- [SocQ CLI and devtools (skill metadata homepage)](https://github.com/SocQAPI/socq-devtools)
- [TikTok Shop endpoint reference](references/platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research summary with optional raw JSONL export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, input scope, credit usage, task status, result count, pagination coverage, and collection caveats when available.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
