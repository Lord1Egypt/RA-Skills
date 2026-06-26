## Description: <br>
Academic literature intelligence toolkit for multi-source paper search, analysis, and knowledge graph building with AI assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, and developers use ScholarGraph to search academic sources, analyze papers, build knowledge graphs, monitor research topics, and generate structured learning or review outputs with AI assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local execution and credential-handling paths need review before installation. <br>
Mitigation: Run the skill in a virtual environment or container, review it as a local code-execution tool, and avoid sharing logs that may contain configuration output. <br>
Risk: Research content may be sent to external AI providers when AI-assisted analysis is enabled. <br>
Mitigation: Do not process confidential or unpublished research with external AI providers unless that is acceptable under the user's policies. <br>
Risk: File processing and output-path behavior may be risky for unusual filenames or paths. <br>
Mitigation: Preinstall optional Python dependencies yourself and avoid processing files or output paths with unusual characters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Josephyb97/scholargraph) <br>
- [Source Repository](https://github.com/Josephyb97/ScholarGraph) <br>
- [README](README.md) <br>
- [Query Expansion](QUERY_EXPANSION.md) <br>
- [Advanced Features](test/ADVANCED_FEATURES.md) <br>
- [Test Results](test/TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, Mermaid, HTML, PPTX, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local files, download PDFs, store SQLite knowledge graphs, and call configured academic and AI provider APIs.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release metadata; artifact metadata also declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
