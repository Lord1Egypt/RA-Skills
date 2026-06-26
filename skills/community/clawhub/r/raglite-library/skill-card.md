## Description: <br>
Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma and hybrid search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirajSanghvi1](https://clawhub.ai/user/VirajSanghvi1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use RAGLite to create a local, auditable retrieval library from private or repeated-use documents, then query it with vector and keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer retrieves executable code from an unpinned GitHub main branch. <br>
Mitigation: Review the upstream repository at installation time, or pin and audit a specific commit before use. <br>
Risk: The skill can process sensitive local documents and store generated Markdown, cache metadata, and Chroma collection data. <br>
Mitigation: Use a dedicated output directory and Chroma collection, protect local storage, and remove generated Markdown, `.raglite` cache data, and Chroma collections when no longer needed. <br>
Risk: The default condensation engine uses OpenClaw unless the user provides another engine. <br>
Mitigation: Explicitly choose a trusted engine and confirm any required gateway and token configuration before processing sensitive documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VirajSanghvi1/raglite-library) <br>
- [Publisher profile](https://clawhub.ai/user/VirajSanghvi1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes distilled Markdown summaries, optional outlines and nodes, index files, and .raglite cache metadata in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact manifest reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
