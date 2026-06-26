## Description: <br>
Query documents on NFS shares, SMB servers, or local drives using local AI with Ollama and ChromaDB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zettabrain](https://clawhub.ai/user/zettabrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT teams, and knowledge workers use this skill to install and run a local RAG workflow over configured document folders and enterprise storage, then ask questions through a CLI or web GUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured document folders are indexed into a local vector store, so sensitive documents may become searchable by anyone with access to the local service or files. <br>
Mitigation: Configure only approved folders, restrict access to the host, and use the documented deletion or rebuild commands to remove indexed data when needed. <br>
Risk: Remote storage or a remote OLLAMA_HOST can move document content, queries, or retrieved chunks off the local machine. <br>
Mitigation: Keep OLLAMA_HOST on localhost for on-device use, and approve any NFS, SMB, S3, or remote Ollama configuration before indexing documents. <br>
Risk: One-line curl or PowerShell installers and service setup execute local installation commands, including sudo on Linux. <br>
Mitigation: Prefer the pipx install path, review installer scripts before running them, and use the documented service disable and uninstall commands when retiring the tool. <br>


## Reference(s): <br>
- [ZettaBrain RAG on ClawHub](https://clawhub.ai/zettabrain/zettabrain-rag) <br>
- [ZettaBrain website](https://zettabrain.io) <br>
- [ZettaBrain RAG GitHub repository](https://github.com/zettabrain/zettabrain-rag) <br>
- [ZettaBrain RAG on PyPI](https://pypi.org/project/zettabrain-rag/) <br>
- [Linux and macOS installer script](https://github.com/zettabrain/zettabrain-rag/blob/main/install.sh) <br>
- [Windows installer script](https://github.com/zettabrain/zettabrain-rag/blob/main/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local document paths, storage backends, service controls, and environment variables configured by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
