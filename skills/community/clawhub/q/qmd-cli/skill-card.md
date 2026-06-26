## Description: <br>
QMD CLI helps agents search and retrieve locally indexed Markdown knowledge bases with BM25 keyword search, vector semantic search, and hybrid search through the qmd CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dpaluy](https://clawhub.ai/user/dpaluy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to query local Markdown notes, documentation, meeting transcripts, and other indexed knowledge bases from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed local notes can contain sensitive information that may be returned to the agent during search or retrieval. <br>
Mitigation: Index only folders intended for agent access and avoid full-document or all-match retrieval on sensitive notes unless that content is intended to enter the conversation. <br>
Risk: The skill depends on an external qmd CLI installation and an MCP server that may expose local indexed content to connected clients. <br>
Mitigation: Install qmd only from a trusted, pinned, or reviewed source and use the MCP server only with trusted clients. <br>


## Reference(s): <br>
- [QMD CLI ClawHub page](https://clawhub.ai/dpaluy/qmd-cli) <br>
- [qmd project](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with qmd shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the qmd --json flag for structured search and retrieval results; MCP mode exposes qmd search and document retrieval tools when enabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
