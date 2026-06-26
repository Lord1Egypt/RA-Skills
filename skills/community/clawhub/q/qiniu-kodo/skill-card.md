## Description: <br>
Qiniu Kodo object storage skill for uploading, downloading, listing, deleting, inspecting, moving, copying, and generating URLs for bucket objects through MCP tools, the Qiniu Node.js SDK, or qshell CLI fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aohoyo](https://clawhub.ai/user/aohoyo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage Qiniu Kodo cloud-storage buckets, including file transfer, listing, metadata lookup, URL generation, and object deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores Qiniu cloud credentials for bucket access. <br>
Mitigation: Use least-privilege Qiniu keys, restrict them to the intended bucket and operations, protect the generated configuration file, and avoid placing secrets in shell startup files. <br>
Risk: The skill can delete or batch-delete remote bucket objects. <br>
Mitigation: Require manual confirmation or a safer wrapper for delete and batch-delete actions, and keep backups for data that should be recoverable. <br>
Risk: The setup script can modify local tool configuration. <br>
Mitigation: Review setup.sh before running it and back up any existing ~/.mcporter/mcporter.json before enabling MCP integration. <br>


## Reference(s): <br>
- [ClawHub qiniu-kodo release page](https://clawhub.ai/aohoyo/qiniu-kodo) <br>
- [Qiniu MCP Server](https://github.com/qiniu/qiniu-mcp-server) <br>
- [Qiniu Node.js SDK](https://developer.qiniu.com/kodo/sdk/1289/nodejs) <br>
- [qshell tool](https://developer.qiniu.com/kodo/tools/1302/qshell) <br>
- [Usage examples](docs/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Node.js, Python, qiniu-mcp-server, qshell, and Qiniu cloud-storage APIs when used by an agent.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
