## Description: <br>
US stocks analysis with AI-synthesized insights that combines price, sentiment, insider trades, congressional STOCK Act disclosures, institutional flows, analyst ratings, and AI signals into read-only, agent-ready briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesentitrader](https://clawhub.ai/user/thesentitrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and synthesize US equities market context from SentiSense APIs, including ticker briefings, smart-money screens, divergence checks, pre-earnings sentiment, and sector rotation summaries. The output should be treated as educational market analysis, not personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ticker and market-analysis queries to SentiSense using a SentiSense API key. <br>
Mitigation: Configure the API key only in trusted agent environments, rotate it if exposed, and monitor request volume against the chosen SentiSense plan. <br>
Risk: Market briefings could be mistaken for personalized investment advice. <br>
Mitigation: Present outputs as educational context and avoid buy, sell, or hold recommendations. <br>
Risk: Quota, rate, or preview-tier limits may truncate or limit returned market data. <br>
Mitigation: State when data is preview-limited or when lookback windows are widened, and synthesize only from returned data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thesentitrader/skills/us-stocks-analysis) <br>
- [SentiSense Website](https://sentisense.ai) <br>
- [SentiSense API Reference](https://sentisense.ai/skill.md) <br>
- [SentiSense App API Base](https://app.sentisense.ai) <br>
- [SentiSense Pricing](https://app.sentisense.ai/pricing?coupon=AGENTS26) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Concise Markdown or plain-text market-analysis briefings with endpoint call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only SentiSense API usage; requires SENTISENSE_API_KEY and may be subject to quota, rate, and preview-tier limits.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
