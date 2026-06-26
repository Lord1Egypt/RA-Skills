## Description: <br>
Local memory semantic search for OpenClaw workspace memory files, using BM25 and multi-signal reranking without external APIs or model dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indivisible2025](https://clawhub.ai/user/indivisible2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to search local memory records, previous decisions, configuration notes, and daily markdown memory files. It is intended for explicit memory or history retrieval where file paths, line ranges, scores, and content previews help the user inspect matching records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate memory search for ambiguous prompts and expose private local memory content. <br>
Mitigation: Use the skill only for explicit memory or history retrieval, tighten trigger rules if needed, and review search output before sharing it. <br>
Risk: The skill creates local memory index and token cache files that can contain searchable representations of private notes. <br>
Mitigation: Review and protect ~/.openclaw/memory_bm25_index.json and ~/.openclaw/memory_bm25_token_cache.json, and remove or rebuild them when the underlying memory files should no longer be searchable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indivisible2025/reminiscence) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results with file paths, line ranges, relevance scores, and content previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against ~/.openclaw/workspace/MEMORY.md and ~/.openclaw/workspace/memory/*.md; builds JSON index and token cache files under ~/.openclaw.] <br>

## Skill Version(s): <br>
7.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
