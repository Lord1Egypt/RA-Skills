## Description: <br>
探针资本出品。中国医疗产业情报引擎，覆盖10万+医疗公司、50万+融资事件、109万条专利、全市场临床试验、A/港/美三地行情。查公司/融资/临床试验/专利/赛道热度/二级市场行情。By Probe Capital. Use when user asks about Chinese healthcare/biotech companies, financing events, clinical trials, patents, sector trends, or market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanjj-cmd](https://clawhub.ai/user/yanjj-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to query Chinese healthcare and biotech companies, financing events, clinical trials, patents, sector trends, daily intelligence, and A/HK/US market data through Sano Intel API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an API token and user queries to an unencrypted HTTP service. <br>
Mitigation: Use only if the provider and network path are trusted; avoid valuable or reused tokens and prefer temporary environment configuration until HTTPS is available. <br>
Risk: Industry intelligence, financing, patent, clinical trial, and market data may be incomplete or stale. <br>
Mitigation: Treat results as research support and verify important investment, clinical, or market conclusions against authoritative sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanjj-cmd/sanointel-by-probevc) <br>
- [Sano Intel API base](http://47.102.196.1:8081) <br>
- [Sano Intel API token application](http://47.102.196.1:5005/apply) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown text with curl commands and concise Chinese summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SANO_TOKEN API token; responses depend on the external Sano Intel HTTP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
