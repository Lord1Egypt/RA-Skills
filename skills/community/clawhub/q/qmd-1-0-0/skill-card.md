## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[instant-picture](https://clawhub.ai/user/instant-picture) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to index selected local files, manage qmd collections, and search them with BM25, vector, or hybrid query modes. It also documents MCP mode for trusted local clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad folders can add secrets or sensitive personal data to the local qmd index. <br>
Mitigation: Index narrow directories, avoid secrets and sensitive personal data, and clear ~/.cache/qmd when the index is no longer needed. <br>
Risk: MCP mode exposes local search capabilities to connected clients. <br>
Mitigation: Use MCP mode only with trusted clients. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/instant-picture/qmd-1-0-0) <br>
- [qmd package source](https://github.com/tobi/qmd) <br>
- [Publisher homepage](https://tobi.lutke.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on user-selected local folders and may use Ollama for embedding and rerank functionality.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
