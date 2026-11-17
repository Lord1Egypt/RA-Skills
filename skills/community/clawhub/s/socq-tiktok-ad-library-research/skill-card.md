## Description:

Helps agents research public TikTok Ad Library ads using SocQ, including endpoint selection, credit estimates, task polling, and result collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and marketing teams use this skill to find and compare public TikTok ads, estimate collection costs, and report findings or raw export locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ receives the API key and submitted research queries.

Mitigation: Confirm the service is trusted before configuring the key, and keep the key out of prompts, URLs, and saved commands.

Risk: Ad hoc CLI installation may introduce supply-chain risk.

Mitigation: Prefer an installed or version-pinned @socq/cli over ad hoc npx execution.

Risk: Large or multi-endpoint collections can consume substantial credits.

Mitigation: Estimate credits, set a result cap, and obtain approval before paid large-volume or multi-endpoint runs.

Risk: Partial pagination or provider failures can make findings incomplete.

Mitigation: Report collection limits and failures; do not claim complete coverage when collection stops early.

## Reference(s):

- [SocQ TikTok Ad Library API documentation](https://docs.socq.ai/api-manual/tiktok-ad-library)
- [SocQ CLI and MCP integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage](https://github.com/SocQAPI/socq-devtools)
- [Supported endpoints and costs](artifact/references/platform.md)
- [Billing and cost control](artifact/references/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSONL exports]

**Output Format:** [Markdown research summary with optional raw JSONL export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, filters, credits, task status, result counts, coverage limits, and collection time when available.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
