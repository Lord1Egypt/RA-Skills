## Description: <br>
八字 MCP 是一款基于 AI 的八字计算器，提供八字排盘数据，用于性格分析和命运预测。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to retrieve Bazi chart details, possible solar times from a Bazi string, and Chinese almanac information for calendar or astrology workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoBenYang API key and stores it in a local .env file. <br>
Mitigation: Treat the .env file as sensitive, avoid using the key on shared machines, and remove or rotate the key when access is no longer needed. <br>
Risk: Bazi and calendar requests can include personal inputs such as birth time and gender that are sent to a third-party service. <br>
Mitigation: Use the skill only with inputs the user agrees to share with XiaoBenYang and avoid sending unnecessary personal data. <br>
Risk: Dependencies are declared with lower-bound version ranges rather than a pinned production set. <br>
Mitigation: Pin and review dependency versions before production or managed deployment. <br>


## Reference(s): <br>
- [XiaoBenYang](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown summary with JSON-derived API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends requested birth or calendar inputs to the XiaoBenYang service.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
