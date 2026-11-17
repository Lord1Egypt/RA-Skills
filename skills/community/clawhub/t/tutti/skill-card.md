## Description:

Orchestrate multiple AI coding agents (Claude Code, Codex, Aider) from a single config to launch teams, run workflows, track capacity, and manage handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutt-adam](https://clawhub.ai/user/nutt-adam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple AI coding agents, run configured workflows, monitor agent status, and manage handoffs or landing work in a repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start agents, run workflows, land branches, open PRs, and execute configured shell-command workflow steps in the active repository.

Mitigation: Install only for trusted repositories, review tutti.toml first, run preflight checks, and require explicit human approval before run_workflow, land_agent --force, land_agent --pr, or workflows that run shell commands or push code.

Risk: Handoff packets and captured agent outputs can contain sensitive project context.

Mitigation: Treat handoff packets as sensitive artifacts and review the target agent and packet path before apply_handoff.

## Reference(s):

- [Tutti homepage](https://github.com/nutthouse/tutti)
- [ClawHub skill page](https://clawhub.ai/nutt-adam/skills/tutti)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON action envelopes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wrapper actions return status, command, stdout, stderr, and parsed data when available.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, action contract, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
