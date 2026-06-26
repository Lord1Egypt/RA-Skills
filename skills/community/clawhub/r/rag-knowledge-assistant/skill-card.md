## Description: <br>
A retrieval-augmented generation knowledge-base assistant that indexes local PDF, Word, Excel, Markdown, and text documents with Chroma and embedding models, then answers questions with source references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aixbinge](https://clawhub.ai/user/aixbinge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to build a local vector index over selected document folders and query those documents through semantic search with cited source snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe GitHub token examples in the push guide may encourage users to place credentials in remote URLs or shell history. <br>
Mitigation: Do not follow token-in-URL examples; use SSH, GitHub CLI, or a credential manager for GitHub authentication. <br>
Risk: The local vectorstore may persist indexed sensitive, secret, or regulated document content. <br>
Mitigation: Index only deliberately selected document folders and treat the generated vectorstore as sensitive persisted data. <br>
Risk: Dependency installation and local script execution can introduce supply-chain or environment risk. <br>
Mitigation: Use a virtual environment and review dependency versions before installation and execution. <br>
Risk: Rebuilding an index can delete the selected output directory. <br>
Mitigation: Confirm the output directory before using rebuild options and keep backups of any important generated data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aixbinge/rag-knowledge-assistant) <br>
- [README](README.md) <br>
- [PDF reading guide](references/pdf_reading.md) <br>
- [Excel reading guide](references/excel_reading.md) <br>
- [Excel analysis guide](references/excel_analysis.md) <br>
- [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3) <br>
- [LangChain](https://github.com/langchain-ai/langchain) <br>
- [Chroma](https://github.com/chroma-core/chroma) <br>
- [Ollama](https://github.com/ollama/ollama) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented guidance with Python commands, YAML configuration, and source-cited answer text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers depend on the indexed local documents, selected embedding model, vectorstore state, retrieval threshold, and top-k settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
