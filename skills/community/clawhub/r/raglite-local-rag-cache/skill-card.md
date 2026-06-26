## Description: <br>
Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma + hybrid search (vector + keyword). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirajSanghvi1](https://clawhub.ai/user/VirajSanghvi1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use RAGLite to condense local or private documents into auditable Markdown, index them in a local Chroma collection, and query them with hybrid vector and keyword retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer pulls the upstream RAGLite package from the GitHub main branch, so installed code may change between installs. <br>
Mitigation: Audit the upstream dependency before use and pin it to a reviewed commit or release when deploying in controlled environments. <br>
Risk: The default OpenClaw engine and configured Chroma endpoint may process document content outside the current agent session. <br>
Mitigation: Use an explicit local or offline engine for sensitive documents, verify gateway and Chroma routing, and run the skill in an isolated environment when handling private data. <br>


## Reference(s): <br>
- [RAGLite ClawHub listing](https://clawhub.ai/VirajSanghvi1/raglite-local-rag-cache) <br>
- [RAGLite GitHub dependency](https://github.com/VirajSanghvi1/raglite) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes distilled summaries, optional outlines and node files, per-document indexes, a root index, and .raglite metadata under the chosen output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
