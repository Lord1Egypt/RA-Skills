## Description: <br>
Deep research on Xiaohongshu topics by searching posts, ranking high-engagement results, and generating insight reports with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PalmPalm7](https://clawhub.ai/user/PalmPalm7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and researchers use this skill to investigate Xiaohongshu topics, analyze trend signals from search result metadata, and produce concise Markdown research reports with links to notable posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Xiaohongshu account through a local MCP service. <br>
Mitigation: Use a dedicated Xiaohongshu account where possible and confirm exactly what the local MCP service can access before running research. <br>
Risk: The skill saves crawled raw data locally without clear retention controls in the artifact. <br>
Mitigation: Avoid sensitive search terms, review the saved data location, and periodically delete or relocate raw crawl data. <br>
Risk: Untrusted keywords could be interpolated into shell commands or API payloads during research workflows. <br>
Mitigation: Quote shell inputs carefully or pass keywords through structured JSON tooling instead of direct shell interpolation. <br>


## Reference(s): <br>
- [Detailed Workflow](references/workflow.md) <br>
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/PalmPalm7/xiaohongshu-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown report with local JSON data files and inline links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores raw posts, analysis output, and metadata under ~/xiaohongshu-research/{keyword}_{YYYYMMDD_HHmm}/.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
