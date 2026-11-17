## Description: <br>
Tool Finder Tool Free helps agents search SkillHub skills and MCP servers, rank results by name match and rating, identify result sources, and produce install-oriented guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover relevant SkillHub skills and MCP servers, compare search results, and receive commands or configuration guidance for installing selected tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages installing discovered skills or MCP servers, which can introduce untrusted packages or unclear provenance. <br>
Mitigation: Review search results, package provenance, target names, paths, and sources before running install commands. <br>
Risk: The optional AGENTS.md auto-trigger block could cause this skill to influence future agent routing more broadly than intended. <br>
Mitigation: Add auto-trigger configuration only after explicit approval and scope it to known tool-search or installation tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tool-finder-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured search or installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked tool results, source labels, installation commands, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
