## Description:

Complete memory system combining Baidu Embedding auto-recall, Git-Notes structured memory, and file-based workspace search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqicxx](https://clawhub.ai/user/xqicxx)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent memory through Baidu embedding recall, Git-Notes structured storage, and workspace file search. It supports remembering preferences, decisions, tasks, and session context across agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent memory capture can store user preferences, decisions, or personal facts without clear notice.

Mitigation: Require explicit opt-in for memory storage and provide review and deletion controls before using the skill with real users.

Risk: Unsafe shell and Python handling may allow attacker-controlled input to execute code.

Mitigation: Review and fix command construction and Python interpolation before installation, then run security tests on memory storage and search paths.

Risk: Sourcing workspace .env files can expose or execute untrusted local configuration.

Mitigation: Load credentials through a trusted secrets mechanism and avoid sourcing unreviewed files from writable workspaces.

Risk: Baidu embedding recall and storage depend on external API credentials and degrade when credentials are missing.

Mitigation: Document degraded mode clearly, verify credential setup before enabling semantic memory, and avoid sending sensitive or regulated content to the embedding service without approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xqicxx/skills/triple-memory-baidu-embedding)
- [Baidu Qianfan Console](https://console.bce.baidu.com/qianfan/)
- [Original Clawdbot Repository](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce memory recall text, storage instructions, status checks, and setup guidance; Baidu embedding functions require API credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
