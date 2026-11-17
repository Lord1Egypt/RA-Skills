## Description:

Research public Apple App Store apps, reviews, and rankings with SocQ, including endpoint selection, credit estimates, asynchronous collection, pagination, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to collect and compare public Apple App Store app details, reviews, and category rankings through SocQ, with cost estimates and coverage notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SocQ API key is provided to the hosted service for requests.

Mitigation: Use this integration only when that access is intended; keep the key in the environment rather than prompts, URLs, or saved commands.

Risk: Large or multi-endpoint requests can incur substantial credit charges.

Mitigation: Check current pricing and expected credits, set a scope cap, and request approval before large paid runs.

Risk: CLI installation and incomplete collections can affect trust in results.

Mitigation: Prefer a vetted or pinned @socq/cli version, and disclose failed requests or pagination gaps instead of claiming complete coverage.

## Reference(s):

- [SocQ Apple App Store API documentation](https://docs.socq.ai/api-manual/apple-app-store)
- [SocQ integration overview](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage (listed in skill metadata)](https://github.com/SocQAPI/socq-devtools)
- [Apple App Store endpoints](references/platform.md)
- [Authentication](references/authentication.md)
- [Billing and cost control](references/billing.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown findings or guidance with optional commands and raw export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, cost, task status, result coverage, and collection time when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
