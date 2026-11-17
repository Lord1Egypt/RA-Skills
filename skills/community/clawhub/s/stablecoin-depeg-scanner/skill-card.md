## Description:

Evaluates stablecoin depeg events for crisis arbitrage opportunities and helps decide whether to buy, watch, or avoid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[june-kris](https://clawhub.ai/user/june-kris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to rapidly evaluate stablecoin depeg incidents, combine market and TVL signals with exploit-response checks, and produce a buy, watch, or avoid recommendation with position sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide fast, prescriptive real-money trading guidance from incomplete or inconsistent collateral evidence.

Mitigation: Treat BUY and position-size outputs as untrusted until collateral status, exploit type, team response, API freshness, and asset identity are independently verified.

Risk: Public market and TVL APIs may be stale or may match the wrong asset or protocol.

Mitigation: Confirm CoinGecko and DefiLlama results against official project channels, block explorers, and security-firm reports before using the recommendation.

Risk: The output language may not match the user's requested language.

Mitigation: Adapt the final response language and formatting to the user's preference before forwarding the assessment.

## Reference(s):

- [Depeg Assessment Decision Framework](artifact/references/decision-framework.md)
- [ClawHub skill page](https://clawhub.ai/june-kris/skills/stablecoin-depeg-scanner)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [DefiLlama API](https://api.llama.fi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style assessment report with command examples, checklist items, market metrics, and recommendation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include BUY, WATCH, or AVOID recommendations, position size, entry range, exit target, stop condition, and manual verification prompts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
