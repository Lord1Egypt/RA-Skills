## Description: <br>
Enhanced Tavily search with intelligent intent recognition, source preferences, critical source validation, and offline report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fundou1081](https://clawhub.ai/user/fundou1081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches with intent-aware domain selection, preferred-source checks, and optional Markdown reports for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and result data are sent to Tavily or a configured Tavily-compatible endpoint. <br>
Mitigation: Use a dedicated Tavily API key and leave TAVILY_BASE_URL unset unless the replacement endpoint is trusted. <br>
Risk: Exported search reports may contain sensitive search queries or result content in local Markdown files. <br>
Mitigation: Avoid report export for sensitive searches unless local files under $HOME/.openclaw/workspace/reports are acceptable. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/fundou1081/tavily-web-seeker) <br>
- [Tavily API endpoint](https://api.tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON search results with text summaries and optional Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are deduplicated and capped at 20; optional reports are written under $HOME/.openclaw/workspace/reports.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
