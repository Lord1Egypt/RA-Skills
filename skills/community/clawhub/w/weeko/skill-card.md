## Description: <br>
Weeko CLI commands for bookmark management, including search, add, update, delete, group organization, and batch operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupy5](https://clawhub.ai/user/occupy5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding assistant users use this skill to manage Weeko bookmarks and groups from the command line, including searching, creating, updating, deleting, organizing, and batch-moving saved items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Weeko API key and gives the agent access to the user's bookmarks and groups. <br>
Mitigation: Install only when the Weeko CLI package is trusted, keep the API key out of logs and prompts, and run weeko logout or rotate the key if the local config may have been exposed. <br>
Risk: The skill can delete bookmarks and groups, and group deletion can remove the bookmarks within that group. <br>
Mitigation: Use --dry-run first, review exact bookmark or group IDs, and require explicit user confirmation before update, delete, group delete, or batch operations. <br>


## Reference(s): <br>
- [Weeko Skill Page](https://clawhub.ai/occupy5/weeko) <br>
- [Weeko Homepage](https://weeko.blog) <br>
- [Weeko CLI Repository](https://github.com/nicepkg/weeko) <br>
- [weeko-cli Package](https://www.npmjs.com/package/weeko-cli) <br>
- [Weeko CLI Command Reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI outputs in JSON, TOON, or pretty text formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports --dry-run for previewing changes and --format toon for token-efficient agent-readable output.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
