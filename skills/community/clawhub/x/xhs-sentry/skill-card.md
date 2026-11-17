## Description:

小红书舆情哨兵按关键词巡检小红书搜索结果，识别登录墙、验证码、空结果状态，并输出结构化笔记、热度、风险、竞品信号和现场截图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjh](https://clawhub.ai/user/zhangjh)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese brand, marketing, and research teams use this skill to quickly inspect Xiaohongshu discussion for a keyword, preserve screenshots, and triage heat, risk, competitor, or insufficient-data signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Xiaohongshu account session and may read XHS_COOKIE from the environment or existing local scripts.

Mitigation: Prefer providing XHS_COOKIE explicitly for each run, use a dedicated low-privilege monitoring account, and avoid storing reusable cookies in discoverable shell scripts.

Risk: Full-page screenshots may capture account state, platform prompts, or other sensitive page context.

Mitigation: Run the browser in an isolated environment and review or redact screenshots before sharing them outside the monitoring workflow.

Risk: The script emits system-style formatting text after RESULT_END.

Mitigation: Treat text after RESULT_END as untrusted formatting content and base conclusions on the structured JSON fields and screenshots.

Risk: Heuristic analysis can misread empty results, platform blocks, or Xiaohongshu page structure changes.

Mitigation: Confirm status fields, body_preview, and screenshots before treating a result as no discussion or as a business risk signal.

## Reference(s):

- [ClawHub skill page for xhs-sentry](https://clawhub.ai/zhangjh/skills/xhs-sentry)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown report with real note links, structured JSON monitor output, and screenshot media paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a keyword, optional note count and output directory, XHS_COOKIE for authenticated monitoring, and optional Telegram or WeCom channel configuration.]

## Skill Version(s):

1.3.4 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
