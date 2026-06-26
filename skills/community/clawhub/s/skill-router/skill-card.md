## Description: <br>
Routes the current task to the most relevant installed skill and suggests new skills only when existing installed skills are insufficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuzc-001](https://clawhub.ai/user/Yuzc-001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose the best installed skill for a task, keep routing advice concise, and move to discovery only when installed capabilities are clearly insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may influence which installed skill an agent chooses. <br>
Mitigation: Treat its output as routing guidance and review the chosen skill when the task has safety, security, or business impact. <br>
Risk: Reuse-first routing can skip new-skill discovery when an installed skill appears sufficient. <br>
Mitigation: Explicitly request discovery when the goal is to search for new candidates despite an available installed option. <br>
Risk: A local preference map could lead to recommending a skill that is not installed in another environment. <br>
Mitigation: Resolve against the user's actual installed skills first and route to discovery when no strong installed match exists. <br>


## Reference(s): <br>
- [Capability Taxonomy](references/capability-taxonomy.md) <br>
- [Resolution Order](references/resolution-order.md) <br>
- [Publish-Safe Runtime Contract](references/publish-safe-runtime-contract.md) <br>
- [Task to Skill Map](references/task-to-skill-map.md) <br>
- [Local Overrides Example](references/local-overrides-example.md) <br>
- [Reminder Policy](references/reminder-policy.md) <br>
- [Micro Routing Examples](references/micro-routing-examples.md) <br>
- [Skill Router v0.1.0 Release Notes](docs.release-notes-v0.1.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Concise Markdown or plain text routing recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a best skill choice, a short rationale, an optional backup, and an immediate next step.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and changelog, released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
