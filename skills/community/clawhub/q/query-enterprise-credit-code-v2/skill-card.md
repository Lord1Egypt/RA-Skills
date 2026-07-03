## Description: <br>
通过企业名称模糊匹配查询企业统一社会信用代码，支持多结果选择和错误提示，适用于工商信息核验和尽调。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daviddatamining](https://clawhub.ai/user/daviddatamining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
中文用户可用此 skill 通过企业名称查询统一社会信用代码，用于招商线索核验、尽调前基础信息收集和工商信息核对。它可引导 agent 完成模糊搜索、企业选择和最终信用代码查询。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names and enterprise IDs are sent to an undocumented HTTP service. <br>
Mitigation: Install only if you trust the publisher and the agent-data.ihdwork.com service with queried company information. <br>
Risk: Confidential due-diligence searches could expose sensitive business interest before the data flow is documented. <br>
Mitigation: Avoid confidential searches until the skill documents the data flow and uses HTTPS or an approved internal endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daviddatamining/query-enterprise-credit-code-v2) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-shaped lookup results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns enterprise name, unified social credit code, and enterprise ID; may ask the user to select from multiple fuzzy matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
