## Description:

Use SwarmVault when the user needs a local-first knowledge vault that writes durable markdown, graph, search, dashboard, review, chat-session, context-pack, task-ledger, static AI export, retrieval, and MCP artifacts to disk from books, notes, transcripts, exports, datasets, slide decks, files, URLs, code, and recurring source workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to operate SwarmVault as a local-first knowledge vault for compiling source material into durable wiki pages, graph artifacts, searchable outputs, review queues, context packs, task ledgers, static AI exports, and MCP-accessible workspace state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global npm CLI that can read and write vault artifacts in projects.

Mitigation: Prefer project-scoped setup, confirm the installed CLI before use, and use SWARMVAULT_OUT or ignore rules to isolate generated outputs.

Risk: Agent hooks and graph-first modes can persist workflow changes and intercept agent searches.

Mitigation: Avoid --scope user and --graph-first until reviewed; inspect install status before enabling hooks or MCP integration.

Risk: Ingest, share, export, and provider workflows can expose sensitive project or source content.

Mitigation: Keep sensitive files such as .env out of ingests and review share, export, and provider settings before publishing or sending content to remote services.

## Reference(s):

- [SwarmVault documentation](https://www.swarmvault.ai/docs)
- [Artifact Reference](references/artifacts.md)
- [Command Reference](references/commands.md)
- [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create or update local vault artifacts, graph exports, static AI export packs, context packs, task ledger entries, chat transcripts, review queues, and MCP configuration.]

## Skill Version(s):

3.20.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
