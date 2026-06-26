## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use Qmd to index selected local files and search them with keyword, vector, hybrid, and document lookup commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad local directories can expose sensitive files in the local search index. <br>
Mitigation: Add narrow, intentional collections and avoid indexing secrets or broad home-directory paths. <br>
Risk: The skill depends on an external qmd package and optional MCP or non-local Ollama endpoints. <br>
Mitigation: Install the package only if trusted, and use MCP mode or remote Ollama endpoints only with clients and servers you trust. <br>


## Reference(s): <br>
- [Qmd package source](https://github.com/tobi/qmd) <br>
- [Publisher homepage](https://tobi.lutke.com) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qmd CLI commands, local indexing paths, search commands, and MCP mode guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
