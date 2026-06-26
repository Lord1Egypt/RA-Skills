## Description: <br>
Queries real-time Solana ecosystem token prices and market overviews when users ask about token prices, market conditions, or supported Solana assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liji3597](https://clawhub.ai/user/liji3597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up supported Solana ecosystem token prices and market overviews, then present informational market data without price predictions or trading recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags undisclosed wallet transfer monitoring through Helius, including a watch mode that can poll continuously until stopped. <br>
Mitigation: Review the skill before installing, use wallet monitoring only when intended, configure HELIUS_API_KEY deliberately, and stop watch mode when the monitoring task is complete. <br>
Risk: Market prices and token risk data can be stale, unavailable, or mistaken and may be misread as financial advice. <br>
Mitigation: Present outputs as informational only, keep the no-prediction and no-trading-advice guardrails, and verify important decisions against authoritative market sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liji3597/solana-market) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON command output, typically summarized by the agent in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node. The skill guidance says repeated price queries may use a 30-second cache.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
