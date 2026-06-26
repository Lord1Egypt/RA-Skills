## Description: <br>
Helps agents query and update TAPD project requirements, defects, tasks, iterations, test cases, comments, statuses, and related Enterprise WeChat notifications through TAPD MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truesnow](https://clawhub.ai/user/truesnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, project managers, and team leads use this skill to inspect TAPD work items, bug status, iteration contents, to-dos, and work summaries, and to request authorized updates such as status changes or comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can touch TAPD business project records and send Enterprise WeChat messages. <br>
Mitigation: Install only for authorized TAPD projects and accounts, and require explicit approval for edits, comments, status changes, messages, and recurring daily notifications. <br>


## Reference(s): <br>
- [Example prompts](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Conversational text or Markdown summaries with MCP tool-call requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request TAPD MCP actions and Enterprise WeChat messages; approvals should gate changes and notifications.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
