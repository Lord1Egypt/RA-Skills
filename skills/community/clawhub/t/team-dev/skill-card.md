## Description: <br>
Multi-agent development team orchestration for spawning, monitoring, reviewing, and cleaning up coding-agent work across Codex, Claude Code, Gemini, and Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VintLin](https://clawhub.ai/user/VintLin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate coding agents through task dispatch, PR-based workflows, CI and review tracking, fixup requests, worktree cleanup, and task-history pruning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spawned coding agents may run with broad local repository and GitHub authority. <br>
Mitigation: Install and run the skill only in isolated development workspaces with repositories and credentials that are acceptable to expose to coding agents; keep final merge approval under human control. <br>
Risk: Prompts, task metadata, review excerpts, and logs can persist locally or be posted to GitHub or Feishu workflows. <br>
Mitigation: Avoid placing secrets or sensitive data in prompts, review logs, or task descriptions, and review retained logs before sharing or archiving them. <br>
Risk: The dev-board can execute local actions when local actions are explicitly enabled. <br>
Mitigation: Bind the dev-board to trusted localhost-only access and avoid enabling local actions on shared machines, public networks, or production systems. <br>
Risk: SubAgent completion markers do not prove that generated code meets the task requirements. <br>
Mitigation: Use the documented post-task review gate: verify the task definition, run at least one real validation command, check required metrics, and request fixup before merge when evidence is insufficient. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/VintLin/team-dev) <br>
- [Main Agent Guidelines](references/AGENTS.md) <br>
- [Agent Adapters](references/agent-adapters.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [State Machine](references/state-machine.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Post-task Review Checklist](references/post-task-review-checklist.md) <br>
- [Dev Board README](scripts/dev-board/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON task records, generated prompts, review summaries, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can launch local agent CLIs, create git worktrees, update task registries, post PR review comments, and retain prompts or logs under local task-history paths.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
