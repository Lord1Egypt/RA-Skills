## Description:

Enables OpenClaw agents to use local QMD hybrid memory search, embeddings, and re-ranking to reduce API-based memory search costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asabovetech](https://clawhub.ai/user/asabovetech)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to set up local memory search over workspace files, refresh indexes and embeddings, estimate savings, and optionally run QMD as a shared MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs mutable third-party QMD code globally.

Mitigation: Run setup only as a normal user, avoid sudo, and review the QMD package and install command before executing setup.

Risk: The skill indexes local OpenClaw workspace data into QMD collections.

Mitigation: Confirm the workspace path and collection scope before setup, and remove or exclude sensitive files from indexed locations.

Risk: The skill may download about 2GB of local models during embedding.

Mitigation: Confirm disk, bandwidth, and model-source expectations before running the initial embedding step.

Risk: The optional QMD MCP server can run as a daemon on localhost.

Mitigation: Start the server only when multi-agent sharing is needed, inspect daemon status, and stop it when shared memory access is no longer required.

## Reference(s):

- [QMD Memory on ClawHub](https://clawhub.ai/asabovetech/skills/qmd-memory)
- [As Above Technologies ClawHub Profile](https://clawhub.ai/user/asabovetech)
- [QMD Project](https://github.com/tobi/qmd)
- [QMD Memory Skill Issues](https://github.com/asabove/qmd-memory-skill/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can install QMD globally, create local collections, index workspace files, generate embeddings, refresh indexes, estimate API cost savings, and start a local MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json, artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
