## Description: <br>
Repo manifest reconciler. Makes repos-manifest.json the single source of truth for repo organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to check repository layout drift, plan or perform manifest-based repo moves, add or move manifest entries, and generate a markdown tree from repos-manifest.json. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can make broad local repository changes, including moving folders and editing manifest, legal, package, or CLAUDE.md files. <br>
Mitigation: Install only from the trusted publisher profile, review manifest paths for unexpected destinations, and run dry-run or planning commands before executing live sync or fix operations. <br>
Risk: Bulk compliance fixes may change legal and package files across local repositories. <br>
Mitigation: Use compliance fix operations only when bulk edits are intended, and review the resulting file changes before committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-repos) <br>
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [Project homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>
- [npm package](https://www.npmjs.com/package/@wipcomputer/wip-repos) <br>
- [CLI source reference](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repos/cli.mjs) <br>
- [MCP server source reference](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repos/mcp-server.mjs) <br>
- [Skill source reference](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repos/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown, plain text, JSON, and CLI or MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform local manifest updates and repository folder moves when invoked through the CLI, module, or MCP tools.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release metadata; artifact package.json reports 1.9.68) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
