## Description:

UEXX Data Cloud answers cryptocurrency market data questions about market sentiment, ETF flows, funding rates, open interest, and long/short ratios using cached UEXX market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanfanscoin](https://clawhub.ai/user/fanfanscoin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to ask natural-language questions about cryptocurrency sentiment and derivatives metrics and receive direct answers from cached UEXX market data. It can provide API examples only when the user explicitly asks for integration details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts https://bbs.uexx.com to obtain and query cryptocurrency market data.

Mitigation: Install only when external UEXX service access is acceptable, and keep the default HTTPS service URL unless a trusted replacement is required.

Risk: The skill automatically creates or reuses a free UEXX API key and saves it locally.

Mitigation: Restrict permissions on ~/.uexx-data-cloud/free_key.json or delete it when the skill is no longer needed.

Risk: Changing UEXX_DATA_BASE_URL can redirect requests and API-key handling to another endpoint.

Mitigation: Do not set UEXX_DATA_BASE_URL to an untrusted or non-HTTPS endpoint.

## Reference(s):

- [UEXX Data Cloud API Catalog](references/api_catalog.md)
- [UEXX API Guide](https://bbs.uexx.com/api/v1/public/api-guide)
- [UEXX Data Cloud Skill on ClawHub](https://clawhub.ai/fanfanscoin/skills/uexx-data-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown and natural-language text, with shell commands or code examples only when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults symbol-level questions to BTCUSDT when no symbol is provided and includes data time or cache age when useful.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
