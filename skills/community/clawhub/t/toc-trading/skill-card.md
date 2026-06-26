## Description: <br>
Toc Trading is a Chinese A-share assistant for simulated trading, stock-pool management, market analysis, and AI stock-picking challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to practice A-share trading workflows, maintain simulated watchlists and positions, review market signals, and generate informational stock recommendations without placing real brokerage trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial recommendations may be inaccurate, incomplete, or unsuitable for a user's real investment decisions. <br>
Mitigation: Treat recommendations and challenge outcomes as informational practice material and require independent financial review before making real trades. <br>
Risk: The skill stores simulated watchlist, holding, trade, recommendation, and challenge records locally. <br>
Mitigation: Run it only in a workspace where local portfolio-simulation records are acceptable, and remove or protect those JSON records according to the user's retention needs. <br>
Risk: Optional market-data access can use a sensitive Tushare API token. <br>
Mitigation: Provide the token through a protected environment variable and avoid sharing logs or configuration that could expose it. <br>
Risk: Scheduled or Feishu-style notifications could distribute simulated trading information more broadly than intended if enabled in deployment. <br>
Mitigation: Review notification recipients and channels before enabling any scheduled push behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuritu/toc-trading) <br>
- [Product design](artifact/docs/product-design.md) <br>
- [Full product design](artifact/docs/product-design-full.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with tables, status messages, simulated trade summaries, and market-analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local JSON records for watchlists, simulated positions, trades, recommendations, and challenge state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
