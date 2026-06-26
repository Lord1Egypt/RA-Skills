## Description: <br>
Six Agent Orchestrator is a multi-agent workflow template that defines six collaboration roles, a six-stage delivery pipeline, token quota monitoring, and role-boundary checks for structured agent teamwork. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan, delegate, execute, verify, fix, and summarize complex work through a defined six-role agent team. It is best suited as a structured workflow template for coding, review, reasoning, monitoring, and token-budget tracking tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes automated token limits, red-line checks, dispatch, and verification more strongly than the local helper scripts can enforce. <br>
Mitigation: Use it as a workflow template, keep a human reviewer in the loop, and treat generated plans, code, and verification reports as proposals that require review. <br>
Risk: Running the helper scripts can write local log or quota JSON files. <br>
Mitigation: Run the scripts in an expected project directory and inspect generated log or quota files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xb19960921/six-agent-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and Python/shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON logs and token quota files when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
