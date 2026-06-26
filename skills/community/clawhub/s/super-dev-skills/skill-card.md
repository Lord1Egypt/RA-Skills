## Description: <br>
SuperDev is a full-stack development workflow suite for requirements discovery, architecture planning, TDD implementation, UI/UX review, supply-chain security checks, and persistent project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weedfire](https://clawhub.ai/user/weedfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use SuperDev to coordinate a multi-role agent workflow across requirements, architecture, implementation, review, security checks, and post-task learning. It is intended for development tasks where an agent should produce plans, code-oriented guidance, review findings, shell commands, configuration, and persistent memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The suite auto-activates broadly and may influence many development tasks, which can make unwanted workflow changes harder to notice. <br>
Mitigation: Review trigger behavior before installation and narrow or disable always-on catch-all activation where it is not needed. <br>
Risk: The memory workflow can preserve project context, user preferences, and past task details across sessions. <br>
Mitigation: Prefer project-scoped memory, inspect and clear .memory regularly, and avoid use in repositories containing secrets or highly confidential information until persistence behavior is reviewed. <br>
Risk: The skill may ask the host agent to generate code, shell commands, configuration, and security guidance that can affect a project. <br>
Mitigation: Review generated changes and commands before execution, then run the project's normal build, test, and security checks. <br>


## Reference(s): <br>
- [SuperDev on ClawHub](https://clawhub.ai/weedfire/super-dev-skills) <br>
- [Publisher profile](https://clawhub.ai/user/weedfire) <br>
- [README](README.md) <br>
- [OpenClaw plugin manifest](openclaw.plugin.json) <br>
- [agent-skills reference](https://github.com/addyosmani/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and structured checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update project memory files and task artifacts when the host agent grants file access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
