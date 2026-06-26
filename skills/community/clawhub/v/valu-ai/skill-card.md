## Description: <br>
ValU AI generates DCF-based stock valuation reports for A-share and selected Hong Kong listed companies, including financial indicators, WACC sensitivity analysis, relative valuation checks, and batch comparison for 2-5 stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoxiang603](https://clawhub.ai/user/gaoxiang603) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze individual A-share or selected Hong Kong stocks, compare small baskets of stocks, and generate Markdown valuation reports for review. The reports are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a DeepSeek API key and sends selected stock symbols plus assembled public market, financial, and news context to DeepSeek. <br>
Mitigation: Run it only where third-party API use is acceptable, keep the API key in environment configuration, and avoid adding private or sensitive context to analysis prompts. <br>
Risk: Quota and usage history are stored locally in plaintext and may include user identifiers. <br>
Mitigation: Use non-sensitive user IDs, restrict access to the user_data directory, and clear local usage data when it is no longer needed. <br>
Risk: Generated valuation reports may be incomplete, stale, or misleading if market data or model assumptions are wrong. <br>
Mitigation: Review the underlying data, assumptions, and disclaimer before relying on a report, and treat outputs as informational rather than investment advice. <br>
Risk: The artifact includes pricing, quota, package, and purchase-tracking behavior. <br>
Mitigation: Confirm pricing and entitlement behavior before enabling commercial use or connecting the skill to any payment workflow. <br>


## Reference(s): <br>
- [Valu Ai on ClawHub](https://clawhub.ai/gaoxiang603/valu-ai) <br>
- [DeepSeek API key setup](https://platform.deepseek.com/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown valuation reports with status dictionaries and saved report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports under reports/ and store quota and usage history under user_data/.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
