## Description: <br>
Search and browse tasks on OpenAnt. Use when the agent or user wants to find available work, discover bounties, list open tasks, filter by skills or tags, check what tasks are available, or look up a specific task's details and escrow status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search OpenAnt tasks, review available bounties, inspect task details, and check escrow status through read-only CLI queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes the latest OpenAnt CLI through npx and may read from the user's authenticated OpenAnt session. <br>
Mitigation: Use it only for browsing tasks and escrow details, and review CLI output before acting on any task. <br>
Risk: Task details, rewards, and escrow state may change after the skill retrieves them. <br>
Mitigation: Refresh task details and escrow status before accepting, applying for, or submitting work through another skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/search-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with OpenAnt CLI commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are read-only and should append --json for structured output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
