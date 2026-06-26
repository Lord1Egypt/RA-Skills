## Description: <br>
Drive the TirOSMAN autonomous multi-agent demo (5 projects x 150 tasks, Jira-like lifecycle, QA approval) from any MCP-aware client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mturac](https://clawhub.ai/user/mturac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill from an MCP-aware client to estimate, start, monitor, resume, approve, reject, and reset a TirOSMAN autonomous multi-agent demo workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the demo can spend model tokens and change demo task records. <br>
Mitigation: Run demo_estimate first, use auto_run only when execution should start, and verify the company_id before reset or QA actions. <br>
Risk: The skill controls a local TirOSMAN MCP server that may require bearer credentials. <br>
Mitigation: Install and use it only when the local TirOSMAN MCP server is trusted and protect TIROSMAN_MCP_API_KEY as a sensitive credential. <br>
Risk: Task transition data can be forwarded through TIROSMAN_DEMO_WEBHOOK_URL. <br>
Mitigation: Set TIROSMAN_DEMO_WEBHOOK_URL only to trusted destinations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mturac/tirosman-demo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [MCP tool calls with text or Markdown status, estimate, board, and QA guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger token spend, demo task record changes, bearer-authenticated local MCP calls, and optional task-transition webhook forwarding.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
