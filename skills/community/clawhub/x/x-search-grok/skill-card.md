## Description: <br>
Search X (Twitter) for account posts, trending topics, or topic discussions using Grok API. Outputs Obsidian-ready Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyue55](https://clawhub.ai/user/wangyue55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to search X/Twitter accounts, trends, and topics through the Grok API, then receive concise Markdown summaries that can be saved or scheduled for watchlist monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: X/Twitter queries and returned content may be sent to xAI through the user's API key. <br>
Mitigation: Use the skill only for searches whose query text and returned content are acceptable to process through xAI, and provide credentials through XAI_API_KEY. <br>
Risk: Saved Markdown output can overwrite same-day files at the selected output path. <br>
Mitigation: Use a dedicated output directory or explicit file path and review saved files when running repeated searches. <br>
Risk: Scheduled watchlist results can be stored locally or delivered to Telegram, Slack, or Discord channels. <br>
Mitigation: Enable scheduled runs and delivery channels only for searches whose results are appropriate to store or share in those services. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wangyue55/x-search-grok) <br>
- [Declared source repository](https://github.com/wangyue55/x-search-skill) <br>
- [xAI Responses API endpoint](https://api.x.ai/v1/responses) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional saved Markdown files and brief progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY; optional output paths can create or overwrite Markdown files for same-day runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
