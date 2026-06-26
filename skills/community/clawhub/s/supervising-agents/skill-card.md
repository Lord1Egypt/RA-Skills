## Description: <br>
Use when YOU are dispatching tasks to subagents (Agent tool, openclaw, parallel workers). You become the supervisor by default. This skill guides how to monitor, intervene, and verify your subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenclove](https://clawhub.ai/user/allenclove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to supervise delegated subagent work through prepare, dispatch, monitor, verify, and report phases. It helps them define deliverables, check progress, intervene on stalled or off-track work, and report evidence-backed outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring commands and evidence checks may inspect files outside the intended delegated task scope. <br>
Mitigation: Limit file and command checks to the relevant project workspace and the deliverables named in the dispatch plan. <br>
Risk: Enabling the skill as a default may make the agent supervise delegated tasks more aggressively across sessions. <br>
Mitigation: Enable it by default only when that supervision posture is desired, and set task budgets and check intervals before dispatch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allenclove/supervising-agents) <br>
- [Publisher profile](https://clawhub.ai/user/allenclove) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with checklists, prompt templates, shell commands, and TypeScript-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; does not define external APIs or credential requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
