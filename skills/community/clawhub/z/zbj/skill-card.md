## Description: <br>
猪八戒网(ZBJ) MCP服务器 - AI智能需求发布、订单管理、服务搜索、类目匹配，连接百万服务商的一站式威客平台 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nylk](https://clawhub.ai/user/nylk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to let an agent interact with ZBJ marketplace workflows, including demand publishing, order lookup, service search, shop search, category matching, seller evaluation, and payment-link retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact marketplace actions such as publishing or closing demands, selecting winners, evaluating sellers, and requesting payment links. <br>
Mitigation: Use a least-privilege ZBJ API key and require human review before any state-changing request is sent. <br>
Risk: Server provenance is unavailable and the security summary notes unclear provenance. <br>
Mitigation: Install only when the publisher handle and third-party status are acceptable for the deployment. <br>
Risk: Credential misuse could expose or abuse ZBJ account access. <br>
Mitigation: Store ZBJ_API_KEY in the environment or a secret manager, rotate it regularly, and avoid embedding it in prompts, files, or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nylk/zbj) <br>
- [ZBJ MCP Homepage](https://zmcp.zbj.com) <br>
- [ZBJ MCP Documentation](https://zmcp.zbj.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZBJ_API_KEY and network access to zmcp.zbj.com over HTTPS.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
