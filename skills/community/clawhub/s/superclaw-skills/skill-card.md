## Description: <br>
SuperClaw is a bundle of 14 agent workflow skills for disciplined AI coding, including TDD, debugging, code review, planning, brainstorming, verification, subagent dispatch, and skill writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gvuckovich](https://clawhub.ai/user/gvuckovich) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill bundle to guide AI coding sessions through repeatable workflows for design, planning, TDD, debugging, code review, parallel agent dispatch, git worktrees, and completion verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle can broadly steer agent behavior across planning, implementation, review, debugging, verification, and git workflows. <br>
Mitigation: Use it with close supervision and require explicit confirmation before high-impact actions such as commits, pushes, PRs, dependency installs, tests, and worktree deletion. <br>
Risk: Some workflows can run project code or shell commands. <br>
Mitigation: Review commands before execution, run them in the intended workspace, and avoid granting broader permissions than the task requires. <br>
Risk: The brainstorming companion can start a local browser helper and may bind to 0.0.0.0. <br>
Mitigation: Start the browser helper only with user consent, prefer local-only binding where possible, and stop the helper when the session no longer needs it. <br>
Risk: Local records such as .events and .superpowers may contain project or preference details. <br>
Mitigation: Treat those files as local records that may contain sensitive context and review them before sharing or publishing workspace contents. <br>


## Reference(s): <br>
- [SuperClaw README](README.md) <br>
- [Codex Tool Mapping](using-superpowers/references/codex-tools.md) <br>
- [Gemini CLI Tool Mapping](using-superpowers/references/gemini-tools.md) <br>
- [SuperClaw ClawHub Listing](https://clawhub.ai/gvuckovich/superclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to edit files, run tests, manage git state, dispatch subagents, or start a local browser companion when the workflow calls for it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
