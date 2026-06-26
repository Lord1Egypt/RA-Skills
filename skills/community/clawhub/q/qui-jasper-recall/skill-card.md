## Description: <br>
Jasper Recall provides retrieval-augmented memory for AI agents, using ChromaDB and SkillBoss API Hub embeddings to index, search, and recall private, shared, and learned memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents searchable memory across prior sessions, project notes, public shared memories, and agent learnings. It is intended for agent workflows that need continuity, memory indexing, recall queries, and controlled sharing between main and sandboxed agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memories, session summaries, and recall queries may be processed by SkillBoss API Hub. <br>
Mitigation: Install only when that processing is acceptable, avoid indexing sensitive content, and review memory files before sharing or syncing. <br>
Risk: Automatic recall can inject unintended memory context into agent prompts. <br>
Mitigation: Keep autoRecall disabled unless explicitly needed; for sandboxed or untrusted agents, set publicOnly true and use an appropriate minScore threshold. <br>
Risk: The HTTP recall server can expose private memory if bound outside localhost or configured to allow private queries. <br>
Mitigation: Keep the server bound to 127.0.0.1 and do not set RECALL_ALLOW_PRIVATE=true on public or shared hosts. <br>
Risk: Security evidence flags under-disclosed privacy and execution risks, including shell-command construction concerns. <br>
Mitigation: Review the installed configuration, keep credentials scoped, and avoid use with untrusted prompts until the shell-command construction issue is fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/qui-jasper-recall) <br>
- [Multi-Agent Mesh Documentation](artifact/docs/MULTI-AGENT-MESH.md) <br>
- [Shared Memory Specification](artifact/docs/SHARED-MEMORY-SPEC.md) <br>
- [Jasper Recall Skill Source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text responses with optional JSON recall results and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inject recalled memory context automatically when autoRecall is enabled; supports public-only and collection-scoped recall.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
