## Description: <br>
Fetch and inspect market data from Sina Finance public webpage resources across multiple market types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzsec](https://clawhub.ai/user/yzsec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to detect A-share, Hong Kong stock, and domestic futures symbols, fetch Sina Finance public webpage quote data, and summarize normalized quote or page metadata fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Sina Finance webpage resources over the network, and those resources may change availability, fields, or coverage. <br>
Mitigation: Review outputs for source availability and field completeness before relying on them for decisions. <br>
Risk: The skill reads local supporting reference files for futures field notes and Chinese futures symbol mapping. <br>
Mitigation: Review the included reference files before deployment and avoid combining the workflow with sensitive local data unless access boundaries are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzsec/sina-market-gsagent) <br>
- [Sina futures normalized fields](references/fields.md) <br>
- [Chinese futures mapping](references/chinese_futures_mapping.json) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn) <br>
- [Sina futures quote pages](https://finance.sina.com.cn/futures/quotes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown responses with optional JSON or table command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market-data fields returned by public Sina Finance webpage resources.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
