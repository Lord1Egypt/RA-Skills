## Description: <br>
CodeGraph Index helps agents pre-index a codebase with tree-sitter so they can query symbols, call graphs, imports, and project structure before reading files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to explore large repositories, locate function or class relationships, summarize project structure, and reduce broad file-scanning during code analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broad repository indexing and create derived code-structure artifacts. <br>
Mitigation: Use it after an explicit request to build or query a code index, and review generated .tree-sitter files before committing or sharing them. <br>
Risk: The workflow may install tree-sitter-cli globally when the tool is missing. <br>
Mitigation: Review and approve installation commands first; prefer a project-local, container, or managed development-environment install when possible. <br>
Risk: Static call-graph results can miss dynamic calls and may overstate dead-code findings. <br>
Mitigation: Treat dead-code output as candidate analysis and confirm findings manually before deleting or refactoring code. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sipoon/sipoon-codegraph-index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, structured summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce tree-sitter index artifacts and optional MCP tool descriptions when supported.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
