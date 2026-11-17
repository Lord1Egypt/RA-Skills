## Description:

Analyzes stock technical indicators and trends with a standalone Python script, and provides guidance for modifying TradingAgentsV2 analyst nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llq20133100095](https://clawhub.ai/user/llq20133100095)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to run command-line technical analysis for a requested stock symbol, review recent prices and indicator signals, and adapt TradingAgentsV2 analyst-node templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled analysis script uses the requested stock symbol in local cache file paths, which can create a local read/write boundary risk.

Mitigation: Validate stock symbols against an allowlist pattern, escape glob input, and enforce cache-directory containment before broad use.

Risk: Generated market analysis may be incorrect or misleading if upstream market data is unavailable, stale, or malformed.

Mitigation: Review data-source status and analysis output before using it for decisions, and treat the report as informational rather than financial advice.

## Reference(s):

- [Technical indicator reference](artifact/indicators-reference.md)
- [ClawHub skill page](https://clawhub.ai/llq20133100095/skills/stock-analysis-lianghua)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs recent OHLCV activity, technical-indicator trends, summary tables, and analyst-node customization guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
