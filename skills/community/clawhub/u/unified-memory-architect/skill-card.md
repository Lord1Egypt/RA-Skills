## Description:

Unified Memory Architect helps OpenClaw agents store, index, and retrieve dream memories using layered organization and hybrid search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mouxangithub](https://clawhub.ai/user/mouxangithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent builders use this skill to manage memory datasets, run CLI or JavaScript queries, inspect memory statistics, and retrieve memories by tag, date, sentiment, entity, language, or full-text search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broad agent-control, persistent-memory, and background-check behavior that could affect an agent workspace beyond memory search.

Mitigation: Review and disable AGENTS, BOOTSTRAP, SOUL, USER, and HEARTBEAT behavior before installation, and use an isolated workspace for evaluation.

Risk: Memory data and scripts may modify or depend on local workspace state.

Mitigation: Back up memory data and verify the source, scripts, and expected file paths before running install, migration, cleanup, or query commands.

Risk: The integration example may expose an API without sufficient access control or network binding safeguards.

Mitigation: Add authentication and bind services to localhost before running API examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mouxangithub/skills/unified-memory-architect)
- [Publisher profile](https://clawhub.ai/user/mouxangithub)
- [Packaged skill documentation](artifact/clawhub/SKILL.md)
- [API documentation](artifact/docs/API.md)
- [Architecture documentation](artifact/docs/ARCHITECTURE.md)
- [Changelog](artifact/github/CHANGELOG.md)
- [Repository listed in package metadata](https://github.com/openclaw/unified-memory-architect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes CLI and JavaScript query workflows for memory statistics, search, filtering, and integration.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/clawhub/skill.json, artifact/github/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
