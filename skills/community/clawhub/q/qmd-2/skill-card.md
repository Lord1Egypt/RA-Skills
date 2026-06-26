## Description: <br>
Search markdown knowledge bases, notes, and documentation using QMD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Satvik374](https://clawhub.ai/user/Satvik374) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search local markdown notes, documentation, and knowledge bases, then retrieve relevant documents or snippets through the QMD CLI or MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown folders added to QMD can become searchable and retrievable by the agent, including sensitive notes if indexed. <br>
Mitigation: Index only markdown folders appropriate for agent access, and exclude secrets or highly private notes. <br>
Risk: The skill depends on an external QMD npm package and optional background server. <br>
Mitigation: Install the QMD package only from a trusted source, review its updates, and run the background server only when needed. <br>


## Reference(s): <br>
- [QMD MCP Server Setup](artifact/references/mcp-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/Satvik374/qmd-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local QMD indexes and MCP tool responses to return markdown search results and document snippets.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
