## Description: <br>
面向中文用户的小红书舆情巡检技能，按关键词抓取搜索结果，判断登录墙、验证码和空结果状态，并输出结构化笔记、热度、风险、竞品信号和现场截图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjh](https://clawhub.ai/user/zhangjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand, marketing, research, and operations users can run quick Xiaohongshu keyword checks for reputation monitoring, competitor observation, trend tracking, and content research. The skill is intended for fast field evidence and initial signal triage rather than rigorous sentiment modeling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse an existing Xiaohongshu session cookie from local scripts without a clear per-run opt-in. <br>
Mitigation: Use a dedicated low-privilege Xiaohongshu account, pass XHS_COOKIE explicitly for each run, and remove or protect old xhs-monitor scripts if reuse is not desired. <br>
Risk: Configured Telegram or WeCom delivery can send report contents and screenshots to those services. <br>
Mitigation: Enable only approved delivery channels and configure them only when sharing the resulting reports and screenshots with those services is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangjh/xhs-sentry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with structured JSON-derived status fields and screenshot media references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes page status, notes, heat and risk summaries, competitor signals, diagnostics, and screenshot paths.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
