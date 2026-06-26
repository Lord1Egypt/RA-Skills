## Description: <br>
股票多条件筛选、热门因子管理、Jiuyan 数据查询和抖音热点分析。提供 17 个 CLI 工具覆盖四大模块。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query, filter, compare, and analyze stock data, manage hot-factor presets, retrieve Jiuyan stock information, and inspect Douyin hotspot data through OpenClaw-triggered CLI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends authenticated requests to a configured stock API service and depends on STOCK_API_KEY as a secret. <br>
Mitigation: Configure the API endpoint over HTTPS, store STOCK_API_KEY only in managed secret configuration, and avoid plaintext HTTP except for isolated local testing. <br>
Risk: The server security summary says credential and activation guidance is too loose for safe default installation. <br>
Mitigation: Install only when the API provider is trusted and use the skill only for explicit market-data, trend-data, or preset-management requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afengzi/stock-filter-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON returned by CLI tools, with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, STOCK_API_BASE_URL, and an API key for authenticated API requests.] <br>

## Skill Version(s): <br>
1.3.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
