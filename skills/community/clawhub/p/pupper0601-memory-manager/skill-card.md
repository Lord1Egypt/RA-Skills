## Description:

Memory Manager gives OpenClaw agents a three-layer memory system for temporary, long-term, and permanent memories with semantic search, compression, identity resolution, and cross-device sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupper0601](https://clawhub.ai/user/pupper0601)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to initialize, search, update, summarize, compress, and synchronize personal or shared AI memory repositories across sessions and devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private memory content and may send selected memory text to the configured embedding provider.

Mitigation: Use only approved embedding providers, avoid storing secrets in memories, and review memory scope before embedding or syncing.

Risk: Installation and setup can modify shell startup files and persist API keys or GitHub tokens.

Mitigation: Prefer a reviewed local install with --no-shell-rc, keep credentials out of shell startup files, and use narrowly scoped tokens.

Risk: GitHub sync can commit or push personal or shared memory files.

Mitigation: Review changed files and remote settings before syncing, and confirm exactly what will be committed before pushing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupper0601/skills/pupper0601-memory-manager)
- [README](artifact/README.md)
- [Technical reference](artifact/reference.md)
- [Memory style guide](artifact/MEMORY_STYLE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python command invocations, and memory-file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local memory files, update vector indexes, call configured embedding APIs, and run Git sync when directed.]

## Skill Version(s):

v3.5.5 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml report 3.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
