## Description: <br>
Provides OpenClaw access instructions for stock quant chart generation, stock market Q&A, natural-language AI stock screening, and WebSocket real-time monitoring signal notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woshixihongtu-cyber](https://clawhub.ai/user/woshixihongtu-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users and developers use this skill to connect an agent to Yingyan/OpenClaw stock APIs for charts, market analysis, natural-language stock searches, limit-up lists, and real-time monitoring signal notifications. The skill also guides users through local credential configuration required for authenticated HTTP and WebSocket access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local API credentials and sends them to the provider during authenticated requests. <br>
Mitigation: Use dedicated limited-scope keys, avoid pasting production secrets into chat, keep config.json out of source control and backups, rotate exposed keys, and prefer environment variables or a secure secret store when possible. <br>
Risk: Financial data and signal outputs may be incorrect, stale, or unsuitable for a user's investment situation. <br>
Mitigation: Treat chart, market analysis, stock search, and monitoring outputs as informational; review source data and apply independent judgment before taking financial action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woshixihongtu-cyber/stockclaw-yingyan) <br>
- [Publisher profile](https://clawhub.ai/user/woshixihongtu-cyber) <br>
- [Yingyan Quant site](https://yingyan.chatface.com/) <br>
- [OpenClaw API reference](reference.md) <br>
- [OpenClaw examples](examples.md) <br>
- [OpenAPI specification](openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with structured stock tables, chart image links, JSON API payloads, and WebSocket connection guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [HTTP stock search results are capped at 20 rows with fixed fields; WebSocket monitoring returns real-time signal-change notifications when available.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
