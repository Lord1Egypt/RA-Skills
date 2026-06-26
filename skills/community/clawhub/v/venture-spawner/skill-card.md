## Description: <br>
Instant agent hiring. Takes job postings from the orchestrator and fills them with properly configured sub-agents. Handles context passing, timeout enforcement, concurrent agent limits, and completion tracking. The bridge between scoping (orchestrator) and execution (sub-agents). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn scoped job postings into coordinated sub-agent work, including context passing, dependency handling, timeout enforcement, and completion tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates sub-agents that may work on git, SSH, outreach, business strategy, resume, or other sensitive context. <br>
Mitigation: Review JOB_BOARD.md entries and supplied context before spawning agents, and avoid including real credentials or unnecessary sensitive files. <br>
Risk: Workspace job state and completion status can be updated based on spawned-agent outputs. <br>
Mitigation: Review completion status, artifacts, and acceptance criteria before relying on results or starting dependent work. <br>
Risk: Broad or duplicate job postings can cause sub-agents to exceed the intended scope. <br>
Mitigation: Keep the configured three-agent concurrency limit and use specific labels, dependencies, timeouts, and acceptance criteria for each job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/venture-spawner) <br>
- [Publisher profile](https://clawhub.ai/user/dodge1218) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status updates and task instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates workspace job board status, agent session keys, artifact links, and completion times.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
