## Description: <br>
Start finishing tasks instead of just organizing them: connect your OpenClaw agent to Unitask (unitask.app) to manage and do your tasks with secure prioritization, tags, time blocks and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfaiz-007](https://clawhub.ai/user/mfaiz-007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an AI agent to a Unitask account through the hosted MCP endpoint, then read, create, update, organize, time-block, and soft-delete tasks with scoped API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can read and change tasks in a user's Unitask account when given a scoped API token. <br>
Mitigation: Create the narrowest token scopes needed, store the API key in a client or agent secret store, and review write actions before execution. <br>
Risk: Delete, merge, move, or time-block apply actions can make consequential changes to a user's task data. <br>
Mitigation: Confirm destructive or compound actions and use preview or dry-run behavior before applying changes. <br>


## Reference(s): <br>
- [Unitask Agent on ClawHub](https://clawhub.ai/mfaiz-007/unitask-agent) <br>
- [Unitask](https://unitask.app) <br>
- [Unitask hosted MCP endpoint](https://unitask.app/api/mcp) <br>
- [Unitask signup](https://unitask.app/signup) <br>
- [README](README.md) <br>
- [Onboarding](ONBOARDING.md) <br>
- [Use Cases](USE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON configuration snippets and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNITASK_API_KEY and uses the hosted HTTPS MCP endpoint.] <br>

## Skill Version(s): <br>
0.18.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
