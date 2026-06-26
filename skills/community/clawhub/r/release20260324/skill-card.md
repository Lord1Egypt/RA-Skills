## Description: <br>
Academic literature discovery and citation network analysis across arXiv, DBLP, Semantic Scholar, Google Scholar, PDFs, BibTeX, and Zotero, with support for graph building, recommendations, monitoring, topic analysis, summaries, and BibTeX/CSV/Markdown/JSON/HTML exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahaowugit](https://clawhub.ai/user/jiahaowugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and external users use this skill to find academic papers, build and inspect citation networks, analyze literature trends, generate summaries, and export research artifacts for reference managers, reports, or interactive graph review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The interactive graph server can expose unauthenticated file-changing APIs. <br>
Mitigation: Run the server only on trusted machines and networks, prefer binding to 127.0.0.1, and remove wildcard CORS before broader deployment. <br>
Risk: LLM and external API features may send PDF, manuscript, reading-list, or graph content to third parties. <br>
Mitigation: Use these features only with content approved for external processing, and avoid private PDFs, unpublished manuscripts, confidential reading lists, or sensitive graph data unless disclosure is acceptable. <br>
Risk: Graph management commands can persist changes to local graph JSON files. <br>
Mitigation: Keep backups before using serve, remove-seed, or remove-paper, especially when editing important research graphs. <br>
Risk: Zotero API keys may be exposed through shell history or process listings when passed directly on the command line. <br>
Mitigation: Prefer safer secret handling where available and avoid passing Zotero API keys directly as command-line arguments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiahaowugit/release20260324) <br>
- [Publisher profile](https://clawhub.ai/user/jiahaowugit) <br>
- [Semantic Scholar API](https://www.semanticscholar.org/product/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML, BibTeX, CSV] <br>
**Output Format:** [Agent guidance with shell commands and structured JSON-oriented CLI outputs; exported artifacts may be JSON, Markdown, BibTeX, CSV, or self-contained HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are designed for non-interactive execution and primarily write local graph, export, or visualization files when output paths are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
