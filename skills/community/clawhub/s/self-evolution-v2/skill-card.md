## Description: <br>
Gives an AI agent a self-review and continuous-improvement workflow modeled on Hermes Agent capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokexiaoguo](https://clawhub.ai/user/luokexiaoguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent self-review rules, new-session recap behavior, and local learning templates to an agent. It is intended for agents that should record corrections, unresolved tasks, knowledge gaps, and follow-up signals across work sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently alter an agent's SOUL.md and change future behavior. <br>
Mitigation: Review and back up SOUL.md before applying the skill, and add explicit confirmation and rollback controls for shared or sensitive environments. <br>
Risk: The skill keeps local records of corrections, task outcomes, unresolved work, and inferred feedback. <br>
Mitigation: Inspect and redact .learnings files regularly, define retention expectations, and avoid sensitive workspaces unless local records are acceptable. <br>
Risk: Persisted lessons may be overbroad, stale, or based on misunderstood feedback. <br>
Mitigation: Keep lessons specific, use the skill's open and closed status tracking, and review entries before syncing them into durable agent behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokexiaoguo/self-evolution-v2) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Windows installation guide](artifact/scripts/README_Windows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append persistent agent rules to SOUL.md and create local .learnings markdown files when applied.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
