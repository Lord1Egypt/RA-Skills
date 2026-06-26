## Description: <br>
Team Planner helps users plan multi-agent AI teams for complex tasks by analyzing requirements, designing team structures, defining roles, and planning collaboration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ghost0118](https://clawhub.ai/user/Ghost0118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, and agent operators use this skill to decide whether a complex task needs one agent or a multi-agent team, then define roles, responsibilities, dependencies, communication patterns, startup prompts, and success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad team-planning language and may recommend unnecessary multi-agent coordination. <br>
Mitigation: Review the single-agent versus multi-agent recommendation before launching agents, and use the smallest team that covers the task. <br>
Risk: Generated roles and startup prompts may spread sensitive or unnecessary context across multiple agents. <br>
Mitigation: Keep each agent narrowly scoped, review startup prompts before use, and avoid including secrets or unrelated private data in shared context. <br>


## Reference(s): <br>
- [Team Planner ClawHub Page](https://clawhub.ai/Ghost0118/team-planner) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plan with structured sections, role definitions, prompt templates, collaboration phases, and success criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ordered startup sequences and example agent prompts; the skill itself does not execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
