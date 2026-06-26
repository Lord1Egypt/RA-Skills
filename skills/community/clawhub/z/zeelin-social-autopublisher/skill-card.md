## Description: <br>
ZeeLin 四平台自运营 — THUQX AutoOps for OpenClaw 0.5（Twitter、微博、小红书、微信公众号草稿）。支持 Hermes agent 风格的参数化编排、dry-run、结构化 JSON 报告与内容落盘；需已登录各平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate, review, and publish coordinated social-media content across X/Twitter, Weibo, Xiaohongshu, and WeChat draft workflows. It supports Hermes-style review and publish phases with dry-run output, reusable content JSON, and structured run summaries before public posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in browser profile and publish or reply publicly on social platforms. <br>
Mitigation: Run review or dry-run first, inspect generated content and JSON summaries, and use publish mode only after explicit approval. <br>
Risk: Recurring cron jobs can schedule ongoing public posts or replies with limited confirmation safeguards. <br>
Mitigation: Create scheduled jobs only when recurring automation is intended, review the schedule and platform scope, and monitor generated reports after each run. <br>
Risk: Generation may send topics or gathered materials to DuckDuckGo and DashScope, and the skill relies on sensitive local credentials or logged-in sessions. <br>
Mitigation: Use an isolated browser profile, keep credentials scoped to the automation environment, avoid sensitive topics, and do not enable insecure SSL settings. <br>


## Reference(s): <br>
- [Hermes Agent Contract](references/hermes-agent-contract.md) <br>
- [Hermes Operator Prompt](references/hermes-operator-prompt.md) <br>
- [Hermes X Growth Operator Prompt](references/hermes-x-growth-operator-prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-social-autopublisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON artifacts such as content, report, summary, and materials files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports review/dry-run and publish modes; generated JSON artifacts are intended for agent status checks and human content review.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
