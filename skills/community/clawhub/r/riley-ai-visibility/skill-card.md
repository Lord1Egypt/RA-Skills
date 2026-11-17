## Description:

Checks whether AI assistants recommend a brand, product, or crypto token in a category and reports visibility, competitor mentions, rankings, lead tiers, and demand signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, GEO/SEO agencies, sales teams, and crypto analysts use this skill to check AI recommendation visibility, compare category share of voice, qualify prospects, and monitor demand signals through the agentexchange.work API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 API calls can spend USDC from a configured wallet.

Mitigation: Use the free samples endpoint first, confirm each paid request, and set wallet or client-side spending limits before enabling paid calls.

Risk: Incorrect endpoint paths or parameters can produce unintended requests or misleading visibility checks.

Mitigation: Use only the documented GET endpoints or the free catalog and samples before making paid requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rccola990-cloud/skills/riley-ai-visibility)
- [Agent Store API Catalog](https://store.agentexchange.work/)
- [Agent Store Samples](https://store.agentexchange.work/samples)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown or plain text with x402 GET request guidance and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve paid USDC x402 requests through agentcash; use free samples first and require confirmation before paid calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
