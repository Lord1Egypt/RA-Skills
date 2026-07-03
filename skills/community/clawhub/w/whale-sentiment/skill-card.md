## Description: <br>
Whale leaderboard sentiment derived from Hyperliquid top traders <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to request paid whale-sentiment data for crypto trade context, especially before large directional positions or as a confirming modifier for entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically spend USDC from the configured EVM wallet when the agent calls the paid endpoint. <br>
Mitigation: Use a dedicated low-balance wallet and require confirmation before allowing paid calls. <br>
Risk: The skill requires access to an EVM private key. <br>
Mitigation: Avoid primary wallet keys and restrict the environment variable to the agent runtime that needs it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/whale-sentiment) <br>
- [Whale Sentiment Endpoint](https://apexrunner.ai/signals/whale-sentiment) <br>
- [Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON sentiment response with fields such as sentiment, score, and top_traders_long_pct] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and can spend USDC from the configured wallet per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
