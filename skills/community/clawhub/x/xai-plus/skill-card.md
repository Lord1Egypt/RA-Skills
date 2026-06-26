## Description: <br>
Search X/Twitter and the web, chat with Grok models using text or images, and analyze X content with xAI's API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mischasigtermans](https://clawhub.ai/user/mischasigtermans) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and external users use this skill to research X posts and web results, chat with Grok models, analyze images, and inspect X content patterns such as voice, trends, and post quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses API keys from other skill configuration entries, which can broaden credential exposure if configuration files are shared or reused. <br>
Mitigation: Use a dedicated, revocable xAI API key for this skill and remove fallback keys from shared configuration when not needed. <br>
Risk: Prompts, screenshots, drafts, and analyzed content are sent to the xAI API and may include sensitive or regulated information. <br>
Mitigation: Avoid submitting confidential, regulated, or proprietary data unless the deployment has approved xAI API use for that data. <br>
Risk: The skill includes detailed guidance for avoiding X spam and AI-detection signals, which could be misused to evade platform moderation. <br>
Mitigation: Use the analysis as quality guidance only and do not rely on it to bypass platform rules, spam controls, or moderation systems. <br>
Risk: Search, trend, and post-quality analysis can be incomplete, stale, or misleading because it depends on model responses and available indexed content. <br>
Mitigation: Review cited results, verify important claims against primary sources, and treat scoring outputs as advisory. <br>


## Reference(s): <br>
- [xAI Plus release page](https://clawhub.ai/mischasigtermans/xai-plus) <br>
- [mischasigtermans publisher profile](https://clawhub.ai/user/mischasigtermans) <br>
- [API Reference](references/api-reference.md) <br>
- [Search Patterns](references/search-patterns.md) <br>
- [Models](references/models.md) <br>
- [Analysis Prompts](references/analysis-prompts.md) <br>
- [X Algorithm](references/x-algorithm.md) <br>
- [xAI console](https://console.x.ai) <br>
- [xAI API base URL](https://api.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, plain text, links, and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an XAI_API_KEY; supports optional model selection, image inputs, raw API output, and JSON output modes.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
