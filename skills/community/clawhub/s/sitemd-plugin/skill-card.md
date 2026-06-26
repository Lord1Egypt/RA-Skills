## Description: <br>
Build and manage websites from Markdown, including page creation, content generation, configuration, validation, and deployment through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyler-berggren](https://clawhub.ai/user/tyler-berggren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and agent operators use this skill to create, edit, validate, clone, and deploy Markdown-based websites through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install-time code downloads a native binary and may execute it while setting up project files. <br>
Mitigation: Install only from a trusted publisher, review the release source and downloaded binary path, and use the skill inside a version-controlled project. <br>
Risk: The skill can modify site content, settings, agent configuration, and deployment state. <br>
Mitigation: Require explicit user confirmation before delete, activate, clone, config, update, auth-key, or deploy actions, and review diffs before publishing. <br>
Risk: Authentication flows expose sensitive credentials through SITEMD_TOKEN, API keys, or magic login URLs. <br>
Mitigation: Treat tokens, API keys, and login URLs as private secrets; do not paste them into public messages, logs, or generated site content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tyler-berggren/sitemd-plugin) <br>
- [sitemd homepage](https://sitemd.cc) <br>
- [sitemd documentation](https://sitemd.cc/docs) <br>
- [Project repository listed in plugin metadata](https://github.com/sitemd-cc/sitemd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, site files, configuration edits, shell commands, MCP tool calls, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify project files and deployment configuration through the sitemd MCP server.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
