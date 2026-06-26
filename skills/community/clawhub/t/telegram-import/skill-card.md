## Description: <br>
Incrementally imports Telegram messages from a local SQLite database into a LanceDB vector store using Qwen3-Embedding-4B embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulu-owo](https://clawhub.ai/user/lulu-owo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to index Telegram message exports for local semantic search or retrieval workflows. It is intended for environments where the operator controls the source SQLite database, LanceDB output folder, and local embedding service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The importer handles privacy-sensitive Telegram message text and sender or group metadata. <br>
Mitigation: Run it only on intended databases and restrict filesystem access to the resulting LanceDB folder and checkpoint files. <br>
Risk: Message text is sent to a localhost embedding API during import. <br>
Mitigation: Use only a local embedding service that you control and trust before indexing private conversations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lulu-owo/telegram-import) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a Python-based local import workflow with checkpointed batch processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
