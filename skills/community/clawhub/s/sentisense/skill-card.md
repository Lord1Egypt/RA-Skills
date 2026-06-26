## Description: <br>
Read-only financial market data API. Stock prices, sentiment, insider trading, institutional flows, politician trades, AI insights. No trading, no purchases, no write operations, no wallet access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesentitrader](https://clawhub.ai/user/thesentitrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Sentisense to retrieve read-only stock prices, market sentiment, insider and institutional flows, politician trades, earnings calendars, market summaries, and AI-generated financial insights for research workflows. Outputs are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial market data and AI-generated insights can be incomplete, delayed, or unsuitable as investment advice. <br>
Mitigation: Treat results as informational, verify important decisions against primary sources, and do not make trades solely from this skill's output. <br>
Risk: The skill requires a SentiSense API key and some endpoints are quota-gated or require a PRO subscription. <br>
Mitigation: Store the key in SENTISENSE_API_KEY, avoid exposing it in prompts or logs, and confirm the account tier and quota before broad data requests. <br>
Risk: Free-tier preview responses can return partial datasets for PRO-gated endpoints. <br>
Mitigation: Check isPreview, previewReason, and totalCount fields when present, and clearly label preview-limited results. <br>


## Reference(s): <br>
- [SentiSense API documentation](https://sentisense.ai/docs/api/) <br>
- [SentiSense website](https://sentisense.ai) <br>
- [Sentisense ClawHub skill page](https://clawhub.ai/thesentitrader/skills/sentisense) <br>
- [SentiSense hosted skill file](https://sentisense.ai/skill.md) <br>
- [Trackers API documentation](https://sentisense.ai/docs/api/trackers) <br>
- [Institution rankings methodology](https://sentisense.ai/methodology#institution-rankings) <br>
- [Python SDK source](https://github.com/SentiSenseApp/sentisense) <br>
- [Node.js SDK source](https://github.com/SentiSenseApp/sentisense-node) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with REST endpoints, curl and SDK examples, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENTISENSE_API_KEY; API calls are read-only and may be rate-limited, quota-gated, or tier-gated.] <br>

## Skill Version(s): <br>
2.2.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
