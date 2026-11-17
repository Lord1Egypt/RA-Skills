## Description:

钉钉悟空邀请码监控，零 token 消耗。自动监控邀请码图片版本变化，支持本地 Tesseract OCR 识别和心跳推送通知。

This skill is ready for commercial/non-commercial use.

## Publisher:

[teenyboy](https://clawhub.ai/user/teenyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor DingTalk Wukong invite-code image updates, run local OCR on downloaded invite images, and receive heartbeat notifications when new invite content appears.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron setup can overwrite or inject persistent scheduled tasks.

Mitigation: Review cron entries before installation, do not run setup as root, back up the existing crontab, validate the requested interval, and remove only entries owned by this skill.

Risk: Heartbeat cron instructions can replace an existing crontab when applied from a temporary file.

Mitigation: Merge heartbeat jobs with the current crontab instead of replacing it, preserve unrelated jobs, and use private state and notification files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teenyboy/skills/wukong-invite-monitor)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [HEARTBEAT.md](artifact/HEARTBEAT.md)
- [Monitored invite image endpoint](https://gw.alicdn.com/imgextra/i4/O1CN010crKwF1CwSYiUnOMc_!!6000000000145-2-tps-1974-540.png?v={version})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands; runtime scripts emit terminal text, JSON notification payloads, logs, state files, and downloaded PNG images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Tesseract OCR when available; scheduled monitoring writes state and log files under the skill directory and /tmp.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
