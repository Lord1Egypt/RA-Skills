## Description: <br>
Queries read-only Umeng U-App core analytics through umeng-cli, including account totals, daily snapshots, active-user, new-user and launch trends, and usage-duration metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer product analytics questions about Umeng U-App properties, such as DAU, new users, launches, total users, and usage duration. It produces guidance and umeng-cli commands for read-only OpenAPI queries, using appkey only where the requested endpoint requires it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to send umeng-cli trace telemetry, including app identifiers, without a clear user consent step. <br>
Mitigation: Do not run umeng-cli trace or send appkey telemetry unless the user explicitly approves that reporting for the session. <br>
Risk: The skill requires sensitive Umeng account credentials through umeng-cli login and appkey-scoped analytics access. <br>
Mitigation: Install umeng-cli only from a trusted source, use a least-privilege Umeng account, and avoid exposing appkeys or cached credentials in logs or shared output. <br>
Risk: Today metrics can be delayed or incomplete, which can make time-sensitive analytics answers misleading. <br>
Mitigation: When the user needs accurate complete data, prefer yesterday or completed-date endpoints and state any freshness limits in the answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-core-index) <br>
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng website](https://www.umeng.com/) <br>
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API call payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires umeng-cli and an authenticated Umeng account; most application-level queries require an appkey.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
