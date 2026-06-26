## Description: <br>
Breaks a fuzzy, high-friction goal into a sequenced quest chain with prerequisite nodes, parallel branches, waiting points, Definitions of Done, and the first three actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to turn a broad personal, study, administrative, home, or project goal into an actionable task map with dependencies, waiting points, concrete done lines, starter actions, and reroute rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated plan can be incomplete or misprioritized if the user provides an unclear goal, missing deadline, or hidden constraints. <br>
Mitigation: Ask the user for the goal, deadline or time window, success definition, resources, constraints, blockers, approvals, and handoffs before relying on the plan. <br>
Risk: For large cross-team schedules, the skill may stay at the planning level and not replace full project management tooling. <br>
Mitigation: Use the output as an initial task map, then transfer owners, dates, dependencies, and status tracking into the team's project management system. <br>
Risk: The skill should not need credentials, account access, broad filesystem permissions, or background access. <br>
Mitigation: Provide only goal details and constraints needed for planning, and do not grant unnecessary credentials or broad access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/quest-chain-decomposer) <br>
- [Publisher Profile](https://clawhub.ai/user/harrylabsj) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown quest-chain plan with objectives, dependencies, Definitions of Done, starter actions, and reroute rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No shell commands, credentials, account access, broad filesystem permissions, or background access are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
