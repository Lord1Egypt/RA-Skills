## Description: <br>
Trading Quant fetches real-time A-share, US stock, Hong Kong stock, and precious-metals market data and produces multi-factor analysis using technical, capital-flow, fundamental, news, and sentiment signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to retrieve public market data, compare multi-source quotes, review capital-flow and anomaly signals, and generate structured trading-analysis outputs. Its outputs are analysis aids and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound calls to public financial-data and news providers. <br>
Mitigation: Run it only in environments where these network calls are acceptable, and review provider access, rate limits, and data-use terms before production use. <br>
Risk: Market scores, sentiment, and signals can be incomplete, delayed, or misleading. <br>
Mitigation: Treat outputs as analysis aids rather than investment advice, and require human review before making trading or portfolio decisions. <br>
Risk: The skill writes local market-data caches, including temporary cache files. <br>
Mitigation: Use a private application cache directory, restrict filesystem permissions, and clear caches according to data-retention requirements. <br>
Risk: Unpinned or optional dependencies may change behavior over time. <br>
Mitigation: Pin and review dependencies in deployment environments, then rerun security and functional checks after updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/trading-quant) <br>
- [Publisher profile](https://clawhub.ai/user/lanyasheng) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command output, with JSON-like structured market-analysis results from the bundled CLI tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reflect live public financial-data providers and local cache state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
