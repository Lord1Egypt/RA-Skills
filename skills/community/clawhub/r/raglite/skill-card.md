## Description: <br>
Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma (vector) + ripgrep (keyword). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirajSanghvi1](https://clawhub.ai/user/VirajSanghvi1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use RAGLite to build a local, auditable retrieval cache for repeated lookup over private or local documents. It supports distilling source material to structured Markdown, indexing it with Chroma and ripgrep, and querying it later with hybrid retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill pulls the raglite-chromadb package from PyPI or a configured package index. <br>
Mitigation: Install only when the package source is trusted and review the package index setting before installation. <br>
Risk: Indexed documents may include private, secret, or regulated information that persists in local output and Chroma storage. <br>
Mitigation: Index only intentional folders, avoid secrets unless storage and deletion paths are understood, and control access to the output directory and Chroma collection. <br>
Risk: Third-party source documents can contain prompt injection text that attempts to influence downstream agent behavior. <br>
Mitigation: Treat retrieved document text as untrusted data and review generated answers or actions before relying on them. <br>


## Reference(s): <br>
- [RAGLite ClawHub page](https://clawhub.ai/VirajSanghvi1/raglite) <br>
- [RAGLite repository listed in skill documentation](https://github.com/VirajSanghvi1/raglite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands; CLI output includes structured Markdown artifacts and query text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, pip, and rg; installs and runs the raglite-chromadb package in a skill-local virtual environment.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata, SKILL.md frontmatter, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
