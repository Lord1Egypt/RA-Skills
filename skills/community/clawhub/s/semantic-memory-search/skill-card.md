## Description: <br>
Adds local vector-driven semantic search for OpenClaw Markdown memory files using memsearch, hybrid dense-vector and BM25 retrieval, SHA-256 deduplication, and local embeddings without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index local Markdown memory files and retrieve relevant memory snippets with semantic and hybrid search instead of keyword-only grep. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill indexes local OpenClaw memory files, which may contain sensitive personal, project, or operational information. <br>
Mitigation: Restrict indexed paths to memory files you approve and review the configured memory path before running indexing commands. <br>
Risk: The release security summary notes documented daily Discord reporting for sensitive memory indexing without clear limits on what leaves the machine. <br>
Mitigation: Disable or remove any Discord notification path unless you explicitly want external reporting and have verified exactly what data is sent. <br>
Risk: Search results are derived from local indexed files and may expose stale or unintended memory content. <br>
Mitigation: Review search results before using them in downstream decisions, prompts, or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/semantic-memory-search) <br>
- [Publisher profile](https://clawhub.ai/user/sunnyhot) <br>
- [memsearch GitHub](https://github.com/zilliztech/memsearch) <br>
- [memsearch documentation](https://zilliztech.github.io/memsearch/) <br>
- [Milvus](https://milvus.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output depends on the user's local indexed memory files and memsearch configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
