## Description: <br>
同花顺Level2数据获取与深度分析工具，支持读取本地同花顺数据、调用行情数据源、生成技术分析和Level2资金流向报告。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[claremouse007](https://clawhub.ai/user/claremouse007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and financial-analysis users can use this skill to inspect Chinese A-share holdings, read local Tonghuashun data when available, fetch supported market data, and generate JSON or Markdown technical analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Administrator process-memory reading, packet capture, MITM, debugger, shared-memory, or protocol-emulation workflows may expose process data or network traffic. <br>
Mitigation: Treat the skill as a Review install, read the code first, and avoid those workflows unless explicitly authorized and operating in an appropriate low-privilege environment. <br>
Risk: The skill can interact with Tushare credentials and market-data services. <br>
Mitigation: Use a dedicated low-privilege Tushare token and keep paid or account-bound market-data access within the relevant service terms. <br>
Risk: Generated stock-analysis reports and strategy suggestions may be incomplete or misleading. <br>
Mitigation: Review generated reports before acting on them and treat outputs as analysis assistance rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/claremouse007/ths-level2) <br>
- [Tonghuashun website](https://www.10jqka.com.cn/) <br>
- [Tushare documentation](https://tushare.pro/document/1) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON result files, Python code examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local Tonghuashun files, an optional Tushare token, and Windows administrator privileges for memory-reading workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact _meta.json, and SKILL.md version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
