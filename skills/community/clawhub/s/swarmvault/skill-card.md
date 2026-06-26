## Description: <br>
Use SwarmVault when the user needs a local-first knowledge vault that writes durable markdown, graph, search, dashboard, review, chat-session, context-pack, task-ledger, static AI export, retrieval, and MCP artifacts to disk from books, notes, transcripts, exports, datasets, slide decks, files, URLs, code, and recurring source workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to set up and operate a local-first SwarmVault workspace that ingests selected sources, compiles durable wiki and graph artifacts, answers questions, builds handoff packs, and exposes vault state through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SwarmVault can persist and index selected files, repos, transcripts, emails, calendars, chats, and exports on disk. <br>
Mitigation: Review selected sources before ingesting them, inspect generated raw/wiki/state artifacts, and use SWARMVAULT_OUT when artifacts should be isolated from the source tree. <br>
Risk: Configured model, embedding, audio, vision, or web-search providers may process confidential vault content. <br>
Mitigation: Review provider settings before ingesting confidential material, prefer local providers when needed, and avoid optional provider-backed tasks for content that should remain local. <br>
Risk: Static exports, graph share bundles, and MCP exposure can disclose compiled vault content beyond the local workspace. <br>
Mitigation: Inspect generated export, share, and MCP-visible artifacts before sharing them or connecting external tools. <br>
Risk: Agent hooks or user-scope installs can trigger background graph refreshes and project configuration edits. <br>
Mitigation: Use install status checks first, enable hooks or user-scope installs only when accepted, and disable or scope graph-first behavior when background refreshes are not desired. <br>


## Reference(s): <br>
- [SwarmVault documentation](https://www.swarmvault.ai/docs) <br>
- [SwarmVault provider documentation](https://www.swarmvault.ai/docs/providers) <br>
- [SwarmVault troubleshooting documentation](https://www.swarmvault.ai/docs/getting-started/troubleshooting) <br>
- [SwarmVault CLI npm package](https://www.npmjs.com/package/@swarmvaultai/cli) <br>
- [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [Command Reference](references/commands.md) <br>
- [Artifact Reference](references/artifacts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of durable local vault artifacts including markdown wiki pages, graph JSON, context packs, chat transcripts, task ledgers, dashboards, static AI exports, and MCP configuration.] <br>

## Skill Version(s): <br>
3.20.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
