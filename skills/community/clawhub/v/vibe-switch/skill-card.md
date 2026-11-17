## Description:

tmux for AI Agents -- Orchestrate multiple AI coding agents in parallel with one command. Run Claude Code, Codex CLI, and Gemini CLI simultaneously on isolated Git branches with seamless context handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianjhang](https://clawhub.ai/user/brianjhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple AI coding agents across isolated Git worktrees, monitor their status, and hand off task context between agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install and run an external CLI with broad local process and repository control.

Mitigation: Review the npm package and source before installing, and install an exact trusted version such as vibe-switch@1.0.2.

Risk: Spawned non-sandboxed agents may read or change repository files and may use their own network or authentication configuration.

Mitigation: Run only trusted agent CLIs, limit repository and credential exposure, and review generated worktrees and changes before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianjhang/skills/vibe-switch)
- [npm package declared in artifact](https://www.npmjs.com/package/vibe-switch)
- [GitHub project link declared in artifact](https://github.com/brianjhang/vibe-switch)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local Git worktrees, branches, task prompts, logs, and agent handoff steps.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
