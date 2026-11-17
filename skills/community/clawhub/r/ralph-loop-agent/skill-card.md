## Description:

Guides OpenClaw agents to orchestrate Ralph Loop planning and building workflows with exec and process tools, TTY-backed coding-agent sessions, completion checks, and operational safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addozhang](https://clawhub.ai/user/addozhang)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agents use this skill to plan, launch, monitor, and complete multi-iteration coding-agent workflows across tools such as OpenCode, Codex, Claude Code, Goose, Pi, and aider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to run and monitor other coding agents through broad command-execution workflows.

Mitigation: Use it only for intended coding-agent automation, run loops in a sandbox or isolated worktree, validate CLI/model/flag values before execution, and monitor process logs.

Risk: Auto-approval flags can reduce safeguards around tool execution.

Mitigation: Avoid --yolo and --dangerously-skip-permissions; prefer sandboxed execution and limited credentials when automation is needed.

Risk: Rollback guidance can include destructive repository commands.

Mitigation: Do not approve git reset --hard unless repository state has been backed up or reviewed.

## Reference(s):

- [Skill page](https://clawhub.ai/addozhang/skills/ralph-loop-agent)
- [OpenClaw documentation](https://openclaw.com/docs)
- [Original Ralph Loop](https://github.com/openclaw/skills/blob/main/skills/jordyvandomselaar/ralph-loop/SKILL.md)
- [Coding Agent](https://github.com/openclaw/skills/blob/main/skills/steipete/coding-agent/SKILL.md)
- [Ralph Wiggum Playbook](https://ralphwiggum.dev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command templates and tool-call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update PROMPT.md, AGENTS.md, IMPLEMENTATION_PLAN.md, and specs files during a Ralph Loop workflow.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
