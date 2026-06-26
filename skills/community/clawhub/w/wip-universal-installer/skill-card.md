## Description: <br>
Reference installer for agent-native software that scans a repository, detects which interfaces it exposes, and installs them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect repositories that follow the Universal Interface conventions and install supported CLI, module, MCP, OpenClaw plugin, skill, and Claude Code hook interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make broad persistent changes to local agent and npm configuration. <br>
Mitigation: Install only repositories and publishers you trust, run --dry-run first, and review the planned npm, MCP, OpenClaw, LDM, and Claude Code configuration changes before applying them. <br>
Risk: Installed repositories can include package scripts, MCP servers, hooks, and plugin files that change local behavior. <br>
Mitigation: Inspect package.json scripts, MCP server files, hook definitions, and plugin manifests before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/wip-universal-installer) <br>
- [Project Homepage](https://github.com/wipcomputer/wip-universal-installer) <br>
- [Universal Interface Specification](https://github.com/wipcomputer/wip-universal-installer/blob/main/SPEC.md) <br>
- [npm Package](https://www.npmjs.com/package/@wipcomputer/universal-installer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and git for normal use.] <br>

## Skill Version(s): <br>
1.9.72 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
