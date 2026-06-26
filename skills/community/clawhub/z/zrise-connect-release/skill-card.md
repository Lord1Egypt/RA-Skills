## Description: <br>
Connects agents to Zrise tasks through XML-RPC and Lobster approval workflows for task analysis, execution, review, and writeback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khoabd](https://clawhub.ai/user/khoabd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and developers use this skill to process Zrise work items with agent-assisted planning, approval checkpoints, task execution, comments, timesheets, and stage updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Zrise business-data changes, including writebacks, timesheet creation, stage transitions, and knowledge-base updates. <br>
Mitigation: Start in a test or tightly controlled workspace, use least-privilege Zrise credentials, avoid real task IDs during onboarding, and require explicit review before any production writeback. <br>
Risk: Credentialed remote access and weak runtime defaults can expose sensitive workflow or Zrise access. <br>
Mitigation: Re-enable verified TLS before production use, configure WORKFLOW_UI_TOKEN, and bind the workflow UI to localhost where possible. <br>


## Reference(s): <br>
- [Zrise Connect Release on ClawHub](https://clawhub.ai/khoabd/zrise-connect-release) <br>
- [README](README.md) <br>
- [Team Onboarding](docs/TEAM_ONBOARDING.md) <br>
- [Workflow Templates](docs/WORKFLOW_TEMPLATES.md) <br>
- [Telegram Integration](docs/TELEGRAM_INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, and generated Zrise task updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task plans, review comments, writeback content, timesheet entries, stage changes, and workflow configuration.] <br>

## Skill Version(s): <br>
3.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
