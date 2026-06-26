## Description: <br>
Tracks in-session work progress for multi-step tasks by registering steps, updating task status, handling cleanup, and guiding task resumption after context changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to keep multi-step work visible, update task state during execution, clean stale work items, and resume remaining work with explicit per-item decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct agents to update or delete task state during cleanup and resume workflows. <br>
Mitigation: Review remaining work before acting on it, keep durable checklist or commit records for important in-progress work, and confirm per-item direction before changing active tasks. <br>
Risk: The skill can cause agents to run GitHub, deploy, SSH, or curl checks in sessions where credentials or production systems may be reachable. <br>
Mitigation: Use it only in repositories and sessions where those checks are intended, prefer read-only status checks, and require explicit human approval before any command that could change external state. <br>
Risk: Broad activation phrases and shared Claude hook/cache behavior may affect workflows beyond simple task tracking. <br>
Mitigation: Review the installed Claude cache and hook behavior before use, and narrow or disable activation patterns in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/wip) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Resume workflow](artifact/resume.md) <br>
- [Claude Code WIP guide](artifact/claude.md) <br>
- [Antigravity WIP tracking](artifact/antigravity.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command and API-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task-list updates, per-item decision prompts, checklist edits, and external status checks.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata and CHANGELOG, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
