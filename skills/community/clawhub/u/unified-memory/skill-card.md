## Description:

Unified Memory V5 provides an AI-agent memory system with context trees, intelligent summarization, knowledge graphs, workflow automation, hybrid search, atomic transactions, and plugin support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mouxangithub](https://clawhub.ai/user/mouxangithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory capture, storage, recall, search, summarization, and synchronization capabilities to AI-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe install guidance, including curl-to-shell paths.

Mitigation: Review installation steps before execution and prefer package-manager or audited local installation commands.

Risk: The skill can automatically capture, recall, persist, and expose memory data through local or network services.

Mitigation: Enable automatic capture, HTTP/API access, and cloud backup only after scoping data retention, access controls, and network exposure.

Risk: The security scan reports reachable shell-command injection through git-related MCP tools and high-risk plugin or sync behavior.

Mitigation: Treat git, plugin, and sync tools as high risk until command execution paths and permissions are reviewed and constrained.

Risk: Cloud backup credentials may be stored locally.

Mitigation: Avoid enabling cloud backup unless credentials are stored securely and backup targets are approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mouxangithub/skills/unified-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke MCP tools and local services that persist, search, synchronize, back up, or expose memory data depending on configuration.]

## Skill Version(s):

5.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
