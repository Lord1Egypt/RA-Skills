## Description: <br>
为 OpenClaw 用户提供股票量化图、行情诊断、自然语言选股、涨停股查询和 WebSocket 实时监控信号接入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woshixihongtu-cyber](https://clawhub.ai/user/woshixihongtu-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to query A-share stock charts, request market analysis, screen stocks from natural-language criteria, check limit-up stocks, and subscribe to live monitoring signal changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores OpenClaw and monitoring API keys in local config.json and sends them to yingyan.chatface.com for authenticated stock queries and monitoring. <br>
Mitigation: Install only if the user trusts yingyan.chatface.com, keep config.json private, avoid committing or sharing credentials, and rotate keys if they may have leaked. <br>
Risk: WebSocket monitoring uses a live URL with an apikey query parameter and can keep a monitoring session open. <br>
Mitigation: Use monitor_api_key only for WebSocket monitoring, avoid exposing URLs that include apikey, and stop monitoring sessions when live signals are no longer needed. <br>
Risk: Stock-analysis outputs and monitoring signals could be mistaken for investment advice. <br>
Mitigation: Present outputs as data-driven analysis, preserve the skill's disclaimer that results do not constitute investment advice, and avoid absolute predictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woshixihongtu-cyber/stockclaw-yingyan3) <br>
- [API Reference](artifact/reference.md) <br>
- [Examples](artifact/examples.md) <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [Yingyan OpenClaw service](https://yingyan.chatface.com/) <br>
- [OpenClaw demo page](https://yingyan.chatface.com/web/openclaw_demo.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured tables, image URLs, JSON-derived summaries, and WebSocket status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user_id and openClaw_api_key for HTTP requests; WebSocket monitoring requires a separate monitor_api_key; natural-language stock screener results are capped at 20 rows.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
