## Description:

Academic literature intelligence toolkit for multi-source paper search, analysis, and knowledge graph building with AI assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developers use ScholarGraph to search academic sources, analyze papers, build knowledge graphs, track research progress, and generate reports or visualizations with AI assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or sensitive configuration may be exposed through configuration commands or local files.

Mitigation: Review configuration output before sharing logs, avoid running config show/init in shared terminals, and use scoped test credentials where possible.

Risk: PDF figure extraction and PPT export may process crafted or untrusted files and paths.

Mitigation: Run these features only in an isolated environment and avoid using untrusted local paths or files.

Risk: Generated HTML may include untrusted paper metadata or content.

Mitigation: Open generated HTML locally only after review, and do not host or share it until the source metadata has been checked.

Risk: Unpinned or broad dependencies can increase supply-chain risk when handling sensitive research or credentials.

Mitigation: Pin dependencies and review the installed package set before production or sensitive use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/josephyb97/skills/scholargraph)
- [Source Repository](https://github.com/Josephyb97/ScholarGraph)
- [README](README.md)
- [Query Expansion Documentation](QUERY_EXPANSION.md)
- [Advanced Features](test/ADVANCED_FEATURES.md)
- [Test Results](test/TEST_RESULTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, Mermaid, HTML, PPTX, SQLite-backed graph data, and CLI/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local files including reports, downloaded PDFs, presentations, graph exports, and configuration.]

## Skill Version(s):

1.4.3 (source: server release metadata; artifact package.json and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
