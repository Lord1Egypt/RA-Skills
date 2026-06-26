## Description: <br>
Semantic search and Q&A over workspace files using Telnyx Storage + AI embeddings. Index your memory, knowledge, and skills for natural language retrieval and AI-powered answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to index selected workspace memory, knowledge, documentation, and skill files into Telnyx Storage, then retrieve relevant context or generate answers with source references through Telnyx AI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured workspace files and user queries may be sent to Telnyx for storage, embedding, search, and LLM inference. <br>
Mitigation: Review config.json before use, narrow the indexed patterns, and add exclusions for secrets, private data, and files that should not leave the workspace. <br>
Risk: The setup workflow can load a local .env file containing TELNYX_API_KEY. <br>
Mitigation: Prefer exporting TELNYX_API_KEY in the environment and inspect any local .env file before running setup.sh. <br>
Risk: Predictable bucket names and automated pruning can expose or remove unintended indexed content if misconfigured. <br>
Mitigation: Choose a non-predictable bucket name for sensitive use and test sync status before enabling automated --prune. <br>


## Reference(s): <br>
- [ClawHub Telnyx Rag skill page](https://clawhub.ai/teamtelnyx/telnyx-rag) <br>
- [teamtelnyx publisher profile](https://clawhub.ai/user/teamtelnyx) <br>
- [Telnyx API keys](https://portal.telnyx.com/#/app/api-keys) <br>
- [Telnyx Cloud Storage](https://telnyx.com/products/cloud-storage) <br>
- [Telnyx AI similarity search API](https://api.telnyx.com/v2/ai/embeddings/similarity-search) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON, and shell command output depending on the invoked script and flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return retrieved context, generated answers, source references, bucket status, sync summaries, and JSON output for scripting.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
