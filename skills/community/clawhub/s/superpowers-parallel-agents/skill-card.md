## Description: <br>
Use when facing 2 or more independent tasks that can be worked on without shared state - dispatches parallel subagents using sessions_spawn for concurrent investigation and execution, adapted for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to split independent debugging, testing, or implementation tasks across parallel subagents, then review and integrate the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel subagents can interfere if they edit the same files or work from shared state. <br>
Mitigation: Assign each subagent a narrow, independent scope, review each summary, check for file conflicts, and run the full test suite before accepting the combined result. <br>
Risk: Nested or delegated agent work may run powerful repository operations or expose sensitive diffs. <br>
Mitigation: Review proposed commands before confirming writes and avoid sending sensitive diffs to fallback reviewer tools unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/superpowers-parallel-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown with code blocks and task prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces coordination guidance for spawning, reviewing, and integrating parallel subagent work.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
