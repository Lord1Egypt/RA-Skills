## Description: <br>
Guides agents through a five-phase root-cause investigation process before implementing a fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when debugging failures and need the agent to reproduce the issue, inspect recent changes, test a single hypothesis, implement only the root-cause fix, and record lessons after resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to persist debugging notes and lessons without clear user control or scoping. <br>
Mitigation: Use it only in workspaces where storing logs and lessons is acceptable, and avoid issues involving secrets, credentials, customer data, or sensitive production details unless the workflow is updated to ask before writing memory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with investigation steps, hypotheses, test plans, and proposed implementation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to persist debugging notes and lessons in workspace memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
