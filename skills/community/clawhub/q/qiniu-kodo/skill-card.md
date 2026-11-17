## Description:

Qiniu Kodo helps agents manage Qiniu Cloud Kodo object storage by uploading, downloading, listing, deleting, inspecting, moving, copying objects, and generating file URLs through MCP, the Node.js SDK, or qshell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[langhuachuanshi](https://clawhub.ai/user/langhuachuanshi)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to automate Qiniu Cloud Kodo object-storage workflows from an agent, including object upload, download, listing, deletion, metadata inspection, moves, copies, and URL generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure from persisted Qiniu keys or shared-shell usage.

Mitigation: Use narrowly scoped Qiniu credentials, avoid long-lived secrets in shared shells, and inspect shell startup files and mcporter configuration before and after setup.

Risk: Cloud data loss from delete or batch-delete operations.

Mitigation: Avoid destructive operations on production buckets unless independent backups exist and the exact bucket, prefix, and object keys have been verified.

Risk: Installation behavior may modify the user environment through global installs, downloads, and shell-profile edits.

Mitigation: Review the setup script before installing, prefer local package installation, and back up shell startup files before allowing setup changes.

## Reference(s):

- [Qiniu Kodo ClawHub skill page](https://clawhub.ai/langhuachuanshi/skills/qiniu-kodo)
- [Qiniu MCP Server](https://github.com/qiniu/qiniu-mcp-server)
- [Qiniu Node.js SDK documentation](https://developer.qiniu.com/kodo/sdk/1289/nodejs)
- [Qiniu qshell tool documentation](https://developer.qiniu.com/kodo/tools/1302/qshell)
- [Usage examples](docs/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Qiniu object-storage actions that depend on configured credentials, bucket, region, domain, and installed Node.js or MCP tooling.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
