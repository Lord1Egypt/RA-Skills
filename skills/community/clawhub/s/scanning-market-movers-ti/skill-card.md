## Description:

Detects significant price movements and unusual volume across crypto markets using price change, volume ratio, and market cap scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to scan cryptocurrency markets for top gainers, losers, and unusual volume spikes, with configurable thresholds, categories, and export formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime behavior depends on referenced scanner scripts or plugins that were not included in the inspected artifact.

Mitigation: Verify the referenced files and dependent market-price-tracker plugin before relying on scan results.

Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk.

Mitigation: Install in a dedicated Python environment and review or pin dependencies before use.

Risk: File export commands could write results to unintended locations.

Mitigation: Provide explicit output paths and review generated JSON or CSV files before sharing them.

## Reference(s):

- [CoinGecko API documentation](https://www.coingecko.com/en/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; scanner results may be displayed as tables or exported as JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable thresholds, category filters, timeframes, and explicit export output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
