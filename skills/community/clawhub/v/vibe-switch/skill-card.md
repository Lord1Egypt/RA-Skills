## Description: <br>
Vibe-Switch orchestrates multiple AI coding agents in parallel, running Claude Code, Codex CLI, and Gemini CLI on isolated Git branches with context handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianjhang](https://clawhub.ai/user/brianjhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple coding-agent CLIs across isolated Git worktrees, monitor their progress, and hand off context between agents during implementation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a third-party npm CLI that can spawn other coding-agent CLIs. <br>
Mitigation: Install only if the npm package publisher is trusted and review spawned-agent configuration before use. <br>
Risk: Spawned agents may have different sandbox and network behavior, and some are documented as non-sandboxed. <br>
Mitigation: Avoid sensitive repositories with non-sandboxed agents and choose an agent whose access model matches the task. <br>
Risk: `vibe clean` is documented to remove completed task logs and worktrees. <br>
Mitigation: Review, commit, or otherwise preserve important work before running cleanup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianjhang/vibe-switch) <br>
- [npm package](https://www.npmjs.com/package/vibe-switch) <br>
- [GitHub repository](https://github.com/brianjhang/vibe-switch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include agent selection, worktree orchestration, handoff, monitoring, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
