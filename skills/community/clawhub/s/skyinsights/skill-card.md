## Description:

Query the CertiK SkyInsights blockchain risk intelligence API to assess wallet and transaction risk, look up on-chain labels and entity details, and run AML screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certik-ai](https://clawhub.ai/user/certik-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and compliance teams use this skill to check blockchain wallet addresses and transactions for risk signals, entity labels, and AML screening results through CertiK SkyInsights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and transaction hashes are sent to CertiK for risk analysis.

Mitigation: Use the skill only with blockchain data approved for external API analysis.

Risk: API keys and secrets are required and could be exposed if stored in shared files.

Mitigation: Prefer environment variables or a managed secret store, and avoid committing .env files.

Risk: The default workflow can run AML screening after a low or none address-risk result.

Mitigation: Review automatic screening behavior if every external compliance query must be explicitly approved.

## Reference(s):

- [CertiK SkyInsights](https://skyinsights.certik.com/)
- [SkyInsights on ClawHub](https://clawhub.ai/certik-ai/skills/skyinsights)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal-friendly text and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKYINSIGHTS_API_KEY and SKYINSIGHTS_API_SECRET; screening may poll for up to 60 seconds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
