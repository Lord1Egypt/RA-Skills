## Description: <br>
Taskr provides persistent cloud task planning and execution for OpenClaw agents, including hierarchical plans, cross-session handoff, user review, audit notes, and retroactive task history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echo-of-machines](https://clawhub.ai/user/echo-of-machines) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use Taskr to create, review, execute, and resume persistent task plans across sessions or agents while keeping task notes as an audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Taskr uses an API key for a cloud task-management service. <br>
Mitigation: Use a scoped or separate API key and project where possible, and rotate the key if it is exposed. <br>
Risk: Task titles, descriptions, and notes are persistent and support cross-agent handoff. <br>
Mitigation: Avoid storing secrets, customer data, or sensitive internal details in Taskr task fields or notes. <br>
Risk: Stale or incomplete task status can mislead users or later agents resuming the work. <br>
Mitigation: Keep task statuses and notes current, and document skipped work with a finding note. <br>


## Reference(s): <br>
- [Taskr homepage](https://taskr.one) <br>
- [Taskr MCP API endpoint](https://taskr.one/api/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/echo-of-machines/taskr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP_API_URL, MCP_USER_API_KEY, and MCP_PROJECT_ID; task and note data persists in the Taskr cloud service.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
