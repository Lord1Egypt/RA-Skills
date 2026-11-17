## Description:

Academic literature discovery and citation network analysis. Multi-source search across arXiv, DBLP, Semantic Scholar, and Google Scholar. Build citation networks (references from PDF parsing, citations from Google Scholar), get recommendations, monitor new papers, analyze topics, parse PDFs, import from Zotero, generate research summaries, export as BibTeX/CSV/Markdown/JSON, and generate interactive HTML graph visualizations. Use when user asks about finding papers, literature review, citation analysis, research trends, or visualizing citation networks.

This skill is for research and development only.

## Publisher:

[jiahaowugit](https://clawhub.ai/user/jiahaowugit)

### License/Terms of Use:

PolyForm Noncommercial License 1.0.0

## Use Case:

Researchers, students, and developer-agents use this skill to discover academic papers, build and inspect citation graphs, analyze research trends, summarize literature, import references, and export graph artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser management server may be exposed more broadly than described.

Mitigation: Use serve mode only on trusted networks, prefer local-only access, and restrict access with host firewall or network controls.

Risk: PDF text can be sent to external LLM providers when LLM keys are configured.

Mitigation: Do not process confidential PDFs with LLM provider keys set unless that disclosure is intended; unset LLM keys to use extractive summaries.

Risk: The tool can modify graph JSON files during graph management operations.

Mitigation: Work on copies or version-controlled graph files before using commands that add, remove, convert, or persist graph changes.

Risk: The installer and CLI depend on networked scholarly APIs and Python packages.

Mitigation: Review and pin dependencies before installation, and expect external API availability, rate limits, and terms to affect results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiahaowugit/skills/release20260324)
- [OpenPaperGraph Skill Instructions](artifact/SKILL.md)
- [OpenPaperGraph README](artifact/README.md)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON and can write BibTeX, CSV, Markdown, JSON, or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Networked scholarly API calls; optional LLM summaries when provider keys are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
