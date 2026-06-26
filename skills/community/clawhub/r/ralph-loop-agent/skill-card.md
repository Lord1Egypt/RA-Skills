## Description: <br>
Guide OpenClaw agents to execute Ralph Wiggum loops using exec and process tools, orchestrating coding agents such as Codex, Claude Code, OpenCode, and Goose with TTY support, planning/building modes, backpressure, sandboxing, and completion checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addozhang](https://clawhub.ai/user/addozhang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, launch, monitor, and complete Ralph Loop workflows for software projects with supported coding CLIs. It helps structure requirements, implementation planning, iterative builds, test backpressure, and completion detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run coding tools that edit, commit, or reset files in a project. <br>
Mitigation: Use a disposable branch or sandbox, set a narrow working directory, and require explicit approval before commits, resets, rollback commands, or credential use. <br>
Risk: Permission-skipping or broad auto-approval flags can reduce user oversight during agent execution. <br>
Mitigation: Avoid --yolo and permission-skipping flags unless the project is isolated and the operator has reviewed the command plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addozhang/ralph-loop-agent) <br>
- [Original Ralph Loop concept](https://github.com/openclaw/skills/blob/main/skills/jordyvandomselaar/ralph-loop/SKILL.md) <br>
- [Coding Agent inspiration](https://github.com/openclaw/skills/blob/main/skills/steipete/coding-agent/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline command examples and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create or update PROMPT.md, AGENTS.md, specs, and IMPLEMENTATION_PLAN.md in the target project.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
