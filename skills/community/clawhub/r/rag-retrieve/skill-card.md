## Description: <br>
Queries a TiDB hybrid vector, BM25, and metadata store for domain-relevant context with version-aware filtering, multi-query expansion, and optional chain-of-retrieval for multi-hop questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlthorn](https://clawhub.ai/user/stephenlthorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to retrieve relevant documentation, codebase passages, and domain context before planning or generation. It is especially useful when version-aware filtering or multi-hop retrieval is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search and reuse private codebase content with insufficient scoping. <br>
Mitigation: Use only controlled corpora, make user_codebase retrieval explicit opt-in, and exclude secrets and unrelated projects from ingestion. <br>
Risk: The skill uses shell-built local HTTP calls. <br>
Mitigation: Review before installing and replace shell-built curl calls with structured HTTP requests before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephenlthorn/rag-retrieve) <br>
- [Publisher profile](https://clawhub.ai/user/stephenlthorn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured retrieval results with passages, metadata, query expansions, token estimates, and optional retrieval trace.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include retrieved chunks from configured corpora and user codebase sources, depending on inputs and corpus scope.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
