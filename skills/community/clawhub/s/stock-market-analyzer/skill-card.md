## Description: <br>
Analyzes Chinese A-share stock data with real-time price queries, opening and closing summaries, technical indicators, trend analysis, and portfolio tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to query Chinese A-share stock prices, technical indicators, opening and closing market summaries, and small portfolio snapshots for market analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the undeclared kimi_finance package for market-data retrieval. <br>
Mitigation: Verify the kimi_finance package source before installation and pin dependency versions for reproducible use. <br>
Risk: The skill can write CSV outputs to local file paths. <br>
Mitigation: Save generated CSV files only to non-sensitive locations and review paths before running analysis. <br>
Risk: Market data and technical indicators may be incomplete, delayed, or unsuitable as sole investment guidance. <br>
Mitigation: Treat outputs as analysis inputs and verify material decisions against authoritative market data and professional review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/stock-market-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown, Python code snippets, JSON-like dictionaries, and optional CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external market-data dependencies and can write CSV outputs to caller-provided paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
