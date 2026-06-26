## Description: <br>
自媒体矩阵管家虾 helps operators monitor multi-account social-media metrics, analyze engagement, detect account or content anomalies, and generate daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social-media operations teams and content managers use this skill to summarize metrics across Douyin, Xiaohongshu, WeChat Channels, Bilibili, and Weibo accounts, flag unusual performance or account-health signals, and prepare markdown matrix reports or scheduling suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input files may contain account performance details, comments, or other operational data that should not be shared unnecessarily. <br>
Mitigation: Use CSV input with only the fields needed for analysis, avoid credentials and unnecessary personal data, and review generated reports before sharing. <br>
Risk: Reports can be shared to Feishu documents or group chats, which may expose account-health or sentiment findings to unintended recipients. <br>
Mitigation: Explicitly confirm document and group-chat destinations before sending results outside the workspace. <br>
Risk: Keyword-based sentiment and anomaly rules can misclassify nuanced comments or normal performance variation. <br>
Mitigation: Treat alerts as review prompts and validate high-impact findings before making operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/social-matrix-manager-claw) <br>
- [Platform metrics reference](references/platform-metrics.md) <br>
- [Content taxonomy reference](references/content-taxonomy.md) <br>
- [Sentiment keywords reference](references/sentiment-keywords.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, tabular summaries, alerts, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local markdown report when the analysis script is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
