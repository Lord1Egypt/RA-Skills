## Description: <br>
SiYuan Note API client for notebook, document, block, asset, search, export, file, and system operations through a local SiYuan API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiwei2027](https://clawhub.ai/user/weiwei2027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-management users use this skill to let an agent read, search, create, update, move, delete, and export content in a local SiYuan workspace. It is suited for authenticated automation of notebooks, documents, blocks, assets, SQL queries, and file operations when the user controls the local SiYuan API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad authenticated changes to a local SiYuan workspace, including document, block, notebook, asset, and file operations. <br>
Mitigation: Install it only for workspaces where agent control is intended, keep config.yaml private, and review create, update, move, delete, export, file, Pandoc, and proxy requests before execution. <br>
Risk: Raw SQL and network proxy features can expose sensitive note data or send trusted local requests to destinations chosen during use. <br>
Mitigation: Review SQL before allowing it, prefer read-only queries when possible, and use the network proxy only for destinations and payloads the user explicitly trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weiwei2027/siyuan) <br>
- [SiYuan API documentation](https://www.siyuan-note.club/apis) <br>
- [SiYuan official repository](https://github.com/siyuan-note/siyuan) <br>
- [Local API reference](artifact/API.md) <br>
- [Configuration example](artifact/config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, shell, YAML, and JSON examples; command-line tools may emit text, Markdown, JSON, files, or exported archives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running local SiYuan instance, API access enabled, and a private config.yaml containing the user's API token.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, frontmatter, and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
