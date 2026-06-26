## Description: <br>
Guides an agent in detecting and repairing logic, syntax, and instruction conflicts during AI gene-evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonicpopo](https://clawhub.ai/user/tonicpopo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add an immune-and-repair posture to long-running agent workflows, including anomaly interception, rollback guidance, and instruction repair when generated fragments behave poorly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs automatic rollback and prompt or instruction repair for agents without clear limits or user approval. <br>
Mitigation: Use it only with explicit approval for repairs or rollbacks, clear logs, and boundaries on what agent state it may change. <br>
Risk: Using it in agents that can modify their own prompts, skills, or long-running task state may introduce unintended behavioral changes. <br>
Mitigation: Review before installing in those agents and require human review of proposed state or instruction changes before they are applied. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonicpopo/xiaowuzi-gene-repair) <br>
- [Publisher profile](https://clawhub.ai/user/tonicpopo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill artifact with no executable files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
