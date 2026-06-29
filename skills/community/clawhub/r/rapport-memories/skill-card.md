## Description: <br>
Extends an OpenClaw agent's memory with semantic search over persistent memory files so it can recall prior decisions, conversations, and context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to build a local searchable memory index for OpenClaw workspaces. It helps agents retrieve prior memory entries, decisions, and conversation context through semantic or fallback keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory indexing can retain sensitive or personal context beyond the original session. <br>
Mitigation: Index only curated memory files, avoid secrets or personal data, review memory content before indexing, and delete /workspace/.rapport-memories and unwanted /workspace/memory entries when the data should be removed. <br>
Risk: Embedding requests can expose memory content to the configured Ollama endpoint if that endpoint is not trusted. <br>
Mitigation: Use a trusted local Ollama endpoint and verify OLLAMA_HOST before indexing or searching memory content. <br>
Risk: Using a prebuilt sandbox image requires trusting the publisher's image contents. <br>
Mitigation: Prefer building the Docker image from the provided artifact source before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carlosdelfino/rapport-memories) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; runtime commands emit text search results and JSON statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local SQLite, ChromaDB, and Markdown memory artifacts under the configured workspace paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
