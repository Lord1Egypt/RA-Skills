## Description:

Tensorlake SDK helps agents look up current Tensorlake sandbox and orchestration documentation before answering questions or writing Python, TypeScript, CLI, or configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooleel](https://clawhub.ai/user/cooleel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building or maintaining agentic systems that rely on Tensorlake sandboxes, durable workflow orchestration, computer-use automation, browser automation, remote development, or related SDK and CLI workflows. The skill routes agents to live Tensorlake docs first and uses bundled snapshots only as a fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a CLI setup path that pipes a remote installer into the shell.

Mitigation: Do not let an agent auto-run the installer; inspect and independently trust the installer source first, or prefer pinned Python or npm package installation.

Risk: The skill can produce outdated API guidance if live docs are unavailable and the bundled snapshots lag behind Tensorlake's current service.

Mitigation: Fetch the live Tensorlake docs index and relevant markdown pages first; use snapshots only when live fetches fail and state that fallback clearly.

Risk: Tensorlake workflows require credentials and may involve sandbox access, hosted execution, or persisted environments.

Mitigation: Use secret managers or environment variables for credentials, never print API keys, and review generated commands before running them against shared or production resources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cooleel/skills/tensorlake-skills)
- [Tensorlake live docs index](https://docs.tensorlake.ai/llms.txt)
- [Tensorlake documentation](https://docs.tensorlake.ai)
- [TensorLake Sandbox SDK Reference](references/sandbox_sdk.md)
- [TensorLake Sandbox Persistence](references/sandbox_persistence.md)
- [Computer Use (Desktop Automation)](references/computer_use.md)
- [TensorLake Sandbox Use Cases](references/sandbox_usecases.md)
- [TensorLake Applications SDK Reference](references/applications_sdk.md)
- [TensorLake Integration Patterns](references/integrations.md)
- [TensorLake Platform Reference](references/platform.md)
- [Tensorlake offline reference index](references/feature_lookup.md)
- [TensorLake Troubleshooting & Production Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples, shell commands, configuration snippets, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to fetch live Tensorlake documentation before producing final guidance; may fall back to bundled reference snapshots if live documentation is unavailable.]

## Skill Version(s):

2.9.0 (source: SKILL.md frontmatter, AGENTS.md version comment, CHANGELOG, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
