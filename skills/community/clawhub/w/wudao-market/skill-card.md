## Description: <br>
Provides A-share market data access for stock search, K-line data, minute data, rankings, market overview, and trading-calendar checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdreamjc](https://clawhub.ai/user/jcdreamjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call documented A-share market-data endpoints for search, historical and intraday prices, rankings, market breadth, and trading-calendar checks. It is not intended for limit-up board analysis, capital-flow analysis, sector rotation, or news intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary marks the release suspicious because bundled workflows may enable high-impact moderation or broad-authority review behavior. <br>
Mitigation: Install only in a trusted workspace, use explicit targets, and confirm any write action before execution. <br>
Risk: The skill requires API credentials and a caller-provided API base URL. <br>
Mitigation: Require LB_API_KEY and LB_API_BASE to be configured explicitly; do not guess the base URL or expose the API key in shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcdreamjc/wudao-market) <br>
- [QuickTiny stock service](https://stock.quicktiny.cn) <br>
- [OpenClaw API base](https://stock.quicktiny.cn/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables; API responses are documented as success/error JSON envelopes.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
