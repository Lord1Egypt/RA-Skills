## Description: <br>
深度研究 Deep Research orchestrates multi-source web, academic, and news research, fact checks findings, and generates bilingual Markdown research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to plan and run comprehensive research, market analysis, competitive analysis, and professional report generation workflows with cited source review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries may be sent to configured third-party search providers. <br>
Mitigation: Avoid entering sensitive topics or credentials in research prompts unless the configured providers are approved for that data. <br>
Risk: Generated reports can include incorrect, stale, or weakly sourced claims. <br>
Mitigation: Treat reports as drafts and independently verify important claims, citations, and source credibility before use. <br>
Risk: The skill saves task state and generated reports to a local deep-research workspace. <br>
Mitigation: Review local output paths and clean up generated files that contain sensitive research topics or proprietary analysis. <br>
Risk: Optional PDF conversion and companion-skill workflows can invoke npx or install/use additional tooling. <br>
Mitigation: Review md-to-pdf and companion-skill installation steps before running them in trusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/research-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/tobewin) <br>
- [arXiv API endpoint referenced by the skill](http://export.arxiv.org/api/query) <br>
- [DuckDuckGo Instant Answer API endpoint referenced by the skill](https://api.duckduckgo.com/?q=QUERY&format=json) <br>
- [Wikipedia summary API endpoint referenced by the skill](https://en.wikipedia.org/api/rest_v1/page/summary/QUERY) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands, JSON task files, and optional PDF conversion guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; saves research task state and generated reports under a local deep-research workspace.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
