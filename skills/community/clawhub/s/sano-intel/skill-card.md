## Description: <br>
探针资本出品。中国医疗产业情报引擎，覆盖10万+医疗公司、50万+融资事件、109万条专利、全市场临床试验、A/港/美三地行情。查公司/融资/临床试验/专利/赛道热度/二级市场行情。By Probe Capital. Use when user asks about Chinese healthcare/biotech companies, financing events, clinical trials, patents, sector trends, or market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanjj-cmd](https://clawhub.ai/user/yanjj-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment, business development, or research analysts use this skill to query Chinese healthcare and biotech company, financing, clinical trial, patent, sector, market, and daily intelligence data through the Sano Intel API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill asks users to send an API token over plain HTTP to a raw IP address. <br>
Mitigation: Use a scoped and revocable token, avoid storing valuable tokens in shell startup files, prefer an HTTPS endpoint when available, and rotate any token already used over the HTTP endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanjj-cmd/sano-intel) <br>
- [API token request form](https://ffmp60ytnq.feishu.cn/share/base/shrcniDTJZknKba0LUeaF5BBuJg) <br>
- [Sano Intel API base endpoint](http://47.102.196.1:8081) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and concise Chinese summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided SANO_TOKEN API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
