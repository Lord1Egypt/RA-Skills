## Description: <br>
悟道 · A股资金分析 helps agents query A-share anomaly detection, capital flow, northbound capital, sector rotation, stock correlation, concept rankings, and concept constituent data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdreamjc](https://clawhub.ai/user/jcdreamjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent inspect Chinese A-share capital movement, sector behavior, stock relationships, and concept-board composition through the documented API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious and reports broad sandbox and approval bypass behavior in the scanned bundle. <br>
Mitigation: Install only from a trusted publisher workflow, keep approval prompts and sandboxing enabled where possible, and review commands before execution. <br>
Risk: The skill depends on an external stock API and bearer-token credentials. <br>
Mitigation: Store LB_API_KEY securely, avoid exposing it in logs or shared transcripts, and verify API responses before relying on market analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jcdreamjc/wudao-analysis) <br>
- [Wudao Stock API](https://stock.quicktiny.cn) <br>
- [OpenClaw API Base](https://stock.quicktiny.cn/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables; API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
