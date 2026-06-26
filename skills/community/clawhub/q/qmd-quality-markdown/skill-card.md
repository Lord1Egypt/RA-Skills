## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to index local files, search them with lexical, vector, or hybrid retrieval, and retrieve relevant document snippets while working with local Markdown and text collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad local folders may include sensitive files in the qmd cache. <br>
Mitigation: Configure narrow collection paths and masks, avoid secrets and broad home or work directories, and clear ~/.cache/qmd when the index is no longer needed. <br>
Risk: MCP mode can expose indexed local content to connected clients. <br>
Mitigation: Enable qmd mcp only for trusted local clients. <br>
Risk: The installed qmd package is an upstream dependency outside the skill artifact. <br>
Mitigation: Review the upstream package and pin or otherwise control the dependency when supply-chain assurance matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sonnenberglauramarie-afk/qmd-quality-markdown) <br>
- [qmd package repository](https://github.com/tobi/qmd) <br>
- [Homepage](https://tobi.lutke.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local qmd indexes, Ollama configuration, MCP mode, and cache paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
