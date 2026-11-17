## Description:

PreToolUse hook that enforces branch discipline, blocks destructive commands, requires repo onboarding before first write, tracks blocked-file retries, and gates PR creation against external repos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate a branch guard for Claude Code or OpenClaw sessions, reducing accidental writes on protected branches and blocking selected destructive commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Machine-wide Claude/OpenClaw hooks can deny tool calls and write local guard state.

Mitigation: Install only when that behavior is intended, keep a documented removal path for the hook, and review retained data under ~/.ldm/state.

Risk: Security evidence reports verified bypasses that weaken the protection users are asked to rely on.

Mitigation: Treat the guard as workflow assistance rather than a strong access-control boundary until the disclosed bypass and state issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-branch-guard)
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit deny messages, SessionStart warnings, and local audit or session-state records when installed as a hook.]

## Skill Version(s):

1.9.72 (source: server release metadata; bundled package version 1.9.84)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
