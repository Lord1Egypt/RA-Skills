## Description: <br>
Research Review Assistant helps an agent retrieve research papers, summarize methods and findings, score relevance, support iterative refinement, and draft literature reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to gather recent literature, compare papers, identify research gaps, and produce structured review drafts for academic writing or grant support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency metadata was flagged by the security evidence as a supply-chain concern. <br>
Mitigation: Audit and correct package dependency entries before installation or deployment. <br>
Risk: The skill can be triggered automatically through a scheduled literature-review command. <br>
Mitigation: Enable scheduled runs only when the user intends recurring literature-review execution. <br>
Risk: Research summaries and relevance scores may be incomplete or misleading if retrieval results are sparse or low quality. <br>
Mitigation: Review generated literature summaries against source papers before using them in manuscripts, grant materials, or decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/research-review-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/jirboy) <br>
- [arXiv API Endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports with tables, paper summaries, trend analysis, references, optional saved files, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports max_papers, summary_length, and iteration_rounds parameters; the artifact also documents optional scheduled review generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
