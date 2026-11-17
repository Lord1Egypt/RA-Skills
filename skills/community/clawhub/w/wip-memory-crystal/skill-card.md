## Description:

Search and manage the shared memory crystal for recall, memory storage, forgetting, status checks, and past-discussion lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through an AI agent to search, store, forget, and inspect shared memory across AI tools. It also guides setup and operation of the local Memory Crystal CLI, MCP server, hooks, and optional relay features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install persistent memory capture through hooks or cron and may continuously capture AI conversations.

Mitigation: Review the install scope before running setup, verify private-mode and capture-off controls, and use dry-run or manual review where available.

Risk: The skill can modify local agent configuration and install persistent local components.

Mitigation: Review proposed configuration changes and shell commands before execution, and install only in environments where that persistence is acceptable.

Risk: The skill may use API keys, 1Password, external embedding providers, or encrypted relay and file-sync flows.

Mitigation: Prefer local embeddings where possible, keep secrets scoped, and enable relay or file sync only after confirming the data-flow implications.

Risk: Server security evidence reports high-risk path traversal and command-injection issues in relay or file-sync paths.

Mitigation: Avoid relay and file-sync use until those issues are fixed and the release has been reviewed again.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-memory-crystal)
- [Memory Crystal README](https://github.com/wipcomputer/memory-crystal/blob/main/README.md)
- [Technical Documentation](https://github.com/wipcomputer/memory-crystal/blob/main/TECHNICAL.md)
- [Relay: Memory Sync](https://github.com/wipcomputer/memory-crystal/blob/main/RELAY.md)
- [Memory Crystal for Enterprise](https://github.com/wipcomputer/memory-crystal/blob/main/README-ENTERPRISE.md)
- [npm Package](https://www.npmjs.com/package/memory-crystal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local CLI commands, MCP configuration changes, and memory-management actions for review before execution.]

## Skill Version(s):

0.7.38 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
