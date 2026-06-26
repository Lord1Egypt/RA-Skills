## Description: <br>
Qmd Memory 1.0.0 configures local QMD hybrid search for OpenClaw memory, including workspace collections, embeddings, refresh commands, and optional shared MCP serving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to replace API-backed memory search with local indexing, hybrid retrieval, and workspace-specific collections. It is intended for agents that need searchable local project memory and optional multi-agent memory sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local workspace indexing may ingest sensitive files, private notes, or secrets. <br>
Mitigation: Review the directories and file masks before setup, exclude sensitive content from scanned paths, and confirm where the local index is stored. <br>
Risk: Recurring or background indexing can keep collecting new workspace content after initial setup. <br>
Mitigation: Enable scheduled refresh only after confirming scope, and document how to stop the schedule and delete the local index. <br>
Risk: The optional MCP server exposes shared memory access on localhost. <br>
Mitigation: Run the server only when multi-agent sharing is needed, keep it local, and stop it when not in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/qmd-memory-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/Sieyer) <br>
- [QMD project](https://github.com/tobi/qmd) <br>
- [QMD Memory support issues](https://github.com/asabove/qmd-memory-skill/issues) <br>
- [As Above Technologies](https://asabove.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local setup, indexing, embedding refresh, cost calculation, and optional MCP server commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
