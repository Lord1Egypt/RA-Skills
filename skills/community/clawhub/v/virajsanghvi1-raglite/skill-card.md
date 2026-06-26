## Description: <br>
Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma + hybrid search (vector + keyword). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirajSanghvi1](https://clawhub.ai/user/VirajSanghvi1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use RAGLite to build a local, auditable retrieval cache for repeated lookup over private notes, documents, runbooks, and other non-training data. It condenses source material into structured Markdown, indexes it into Chroma, and supports hybrid vector and keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer pulls executable code from a mutable upstream branch. <br>
Mitigation: Review the upstream repository before installing and prefer a pinned commit or released package when deploying the skill. <br>
Risk: The skill can process sensitive documents into a durable searchable cache and may use configured OpenClaw or Chroma services. <br>
Mitigation: Run it only on folders approved for indexing and confirm whether the OpenClaw gateway and Chroma server are local or remote before using sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/VirajSanghvi1/virajsanghvi1-raglite) <br>
- [Publisher profile](https://clawhub.ai/user/VirajSanghvi1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown files, shell command output, and local index metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes distilled summaries, execution notes, optional outlines, node Markdown files, index files, and .raglite metadata under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
