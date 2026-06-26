## Description: <br>
Scholar Deep Research runs an 8-phase, script-driven academic research workflow across OpenAlex, arXiv, Crossref, and PubMed to produce structured reports with deduplication, ranking, citation chasing, self-critique, and verifiable citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical teams use this skill to turn scholarly questions into auditable literature reviews, systematic or scoping reviews, comparative analyses, and grant background reports with citations and bibliographies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow checks for Git updates during normal use and may fast-forward a git-installed copy. <br>
Mitigation: Review before installing; use a package-managed release or set SCHOLAR_SKIP_UPDATE_CHECK=1 and pin a reviewed commit when reproducibility or change control matters. <br>
Risk: The skill makes outbound requests to scholarly APIs and may store research topics, papers, cache entries, and state locally. <br>
Mitigation: Keep generated state and cache files private for sensitive topics, and avoid optional personal API keys or email settings unless the user accepts sharing them with the named services. <br>
Risk: Research output can reflect source limitations such as preprints, metadata errors, abstract-only papers, and missing paywalled literature. <br>
Mitigation: Use the built-in quality assessment, citation checks, and self-critique phase; mark preprints or abstract-only sources and disclose database coverage limits in the report. <br>
Risk: The artifact includes optional payment or donation links. <br>
Mitigation: Treat those links as author-support links only; do not authorize payments or purchases as part of running the research workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agents365-ai/scholar-deep-research) <br>
- [Publisher profile](https://clawhub.ai/user/agents365-ai) <br>
- [Project website](https://agents365-ai.github.io/scholar-deep-research/) <br>
- [Search strategies](references/search_strategies.md) <br>
- [Source selection](references/source_selection.md) <br>
- [Quality assessment](references/quality_assessment.md) <br>
- [Report templates](references/report_templates.md) <br>
- [Research pitfalls](references/pitfalls.md) <br>
- [Paper Fetch DOI resolver](https://github.com/Agents365-ai/paper-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, bibliography files, JSON workflow state and envelopes, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under reports/<slug>_<YYYYMMDD>.md with generated BibTeX, CSL-JSON, or RIS bibliographies when requested.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
