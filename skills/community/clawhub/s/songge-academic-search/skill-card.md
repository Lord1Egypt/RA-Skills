## Description: <br>
学术论文检索小助手（松哥版）。支持多源检索（OpenAlex/Semantic Scholar/Crossref/arXiv/PubMed），自动补全论文元数据，输出 BibTeX/RIS/JSON/Markdown 引用格式。当用户搜索学术论文、查找文献、生成参考文献列表时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to search academic literature across OpenAlex, Semantic Scholar, Crossref, arXiv, and PubMed, enrich paper metadata, and export references for writing or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are specified with lower bounds, so later package releases could change behavior or introduce dependency risk. <br>
Mitigation: Install in a virtual environment and pin reviewed dependency versions before operational use. <br>
Risk: Semantic Scholar API keys can appear in shell history or transcripts when passed as command-line arguments. <br>
Mitigation: Pass a dedicated key only when needed and avoid shared shells, saved transcripts, or command history exposure. <br>
Risk: Search exports and PDF downloads write files to user-selected paths. <br>
Mitigation: Use a dedicated output folder for citation files and PDFs, then review generated files before sharing or ingesting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingsunzhang2026-oss/songge-academic-search) <br>
- [学术论文检索小助手 - 使用说明](references/readme.md) <br>
- [Semantic Scholar API](https://www.semanticscholar.org/product/api) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [Crossref API](https://api.crossref.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Plain text, JSON, BibTeX, RIS, Markdown, and downloaded PDF files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write citation exports to a requested output path and download arXiv PDFs to a user-selected directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
