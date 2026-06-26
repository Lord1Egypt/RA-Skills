## Description: <br>
Generate and read XMind (.xmind) files via the published xmind-generator-mcp MCP server (npm), with a chat-first UX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BangyiZhang](https://clawhub.ai/user/BangyiZhang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to generate real XMind mind-map files from outlines, plans, PRDs, or test plans, and to read attached XMind files before optionally exporting them to Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a pinned npm MCP package through npx and can create local files. <br>
Mitigation: Use it only when comfortable running xmind-generator-mcp@0.1.2 locally, keep the package version pinned, and review generated files before relying on or sharing them. <br>
Risk: Sensitive content may be included in generated mind maps or chat attachments. <br>
Mitigation: Avoid sensitive inputs unless the local MCP package and attachment handling are trusted, and specify an output path when files should not be saved to the default Desktop location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BangyiZhang/xmind-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON tool arguments, shell command examples, and generated .xmind file attachments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and npx. Generated files default to ~/Desktop when no output path is supplied; filenames are sanitized and generated topic language should match the user's request unless specified.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
