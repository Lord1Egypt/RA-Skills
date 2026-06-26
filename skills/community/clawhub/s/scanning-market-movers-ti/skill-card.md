## Description: <br>
Detect significant price movements and unusual volume across crypto markets, with significance scores combining price change, volume ratio, and market cap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to scan cryptocurrency markets for top gainers, losers, and volume spikes, then prioritize assets with configurable thresholds and significance scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt an agent to run Python-based cryptocurrency market scans and depends on a separate market-price-tracker capability. <br>
Mitigation: Use explicit crypto-market prompts, install and review the market-price-tracker dependency separately, and review outputs before using them for decisions. <br>
Risk: The skill supports local JSON and CSV exports, and overwrite protection for --output paths is not described. <br>
Mitigation: Choose reviewed export paths and check for existing files before running commands that write output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sarkcesscrewpay/scanning-market-movers-ti) <br>
- [Publisher Profile](https://clawhub.ai/user/sarkcesscrewpay) <br>
- [CoinGecko API Documentation](https://www.coingecko.com/en/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, tabular market scan output, JSON, and CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable thresholds, market-cap filters, category filters, timeframes, presets, and local exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
