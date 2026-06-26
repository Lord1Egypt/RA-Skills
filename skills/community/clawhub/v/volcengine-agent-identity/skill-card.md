## Description: <br>
Supports Volcengine UserPool login, TIP tokens, credential hosting, environment bindings, and tool risk approval for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loveyana](https://clawhub.ai/user/loveyana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to authenticate an agent through Volcengine UserPool, manage hosted credentials, bind credentials to tool environment variables, and review high-risk tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-managed credentials may expose raw credential values or persist environment bindings. <br>
Mitigation: Prefer environment binding over returnValue:true, avoid asking the agent to reveal raw credentials, and review provider scopes and env var names before use. <br>
Risk: High-risk tool calls can affect files, commands, or credentials if approvals are not controlled. <br>
Mitigation: Keep high-risk tool approvals under direct human control and do not allow the agent to self-approve approval requests. <br>


## Reference(s): <br>
- [Volcengine Agent Identity and Permission Management](https://www.volcengine.com/docs/86848) <br>
- [ClawHub Skill Page](https://clawhub.ai/loveyana/volcengine-agent-identity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool parameters, JSON status or configuration responses, and authentication URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose raw credential values only when the documented returnValue option is requested.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
