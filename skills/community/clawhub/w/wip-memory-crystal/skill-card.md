## Description: <br>
Memory Crystal Private helps agents search, store, forget, and inspect a private shared memory layer for AI conversations and durable facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect Memory Crystal to agent tools, then search prior conversations, store durable facts, forget selected memory, and inspect memory status across supported clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a persistent memory layer that captures and indexes AI conversations by default. <br>
Mitigation: Install only when persistent capture is desired, and review cron capture, Claude/OpenClaw hooks, private-mode controls, and memory deletion behavior before enabling it. <br>
Risk: Embedding providers, OAuth flows, sensitive credentials, and optional hosted relay configuration can affect privacy and data movement. <br>
Mitigation: Review API key setup, OAuth tokens, embedding provider choice, and relay configuration; use local embeddings or self-hosted relay options when data residency or privacy requirements demand them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-memory-crystal) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [README](README.md) <br>
- [Technical documentation](TECHNICAL.md) <br>
- [Enterprise notes](README-ENTERPRISE.md) <br>
- [Cloud setup notes](cloud/README.md) <br>
- [npm package](https://www.npmjs.com/package/memory-crystal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local CLI, MCP, hook, cron, embedding provider, and relay configuration changes for user review before execution.] <br>

## Skill Version(s): <br>
0.7.38 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
