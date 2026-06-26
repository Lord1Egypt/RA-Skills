## Description: <br>
按代码与时间范围查历史日线，或查列表与详情，便于 K 线与走势分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to retrieve historical daily stock data, stock lists, and stock details for K-line and price trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock lookup parameters and the configured JisuAPI AppKey are sent to JisuAPI when the skill runs. <br>
Mitigation: Use an approved JisuAPI key, avoid including unrelated sensitive information in lookup parameters, and install only when external JisuAPI processing is acceptable. <br>
Risk: Ambiguous stock-market questions can trigger unnecessary or incorrect external API calls. <br>
Mitigation: Confirm the target stock code and date range before running the lookup when the user's request is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/stockhistory) <br>
- [Publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI stock history documentation](https://www.jisuapi.com/api/stockhistory/) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown usage guidance, shell command snippets, and JSON responses from stock history, list, and detail lookups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; lookup requests are sent to the disclosed JisuAPI stockhistory service.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
