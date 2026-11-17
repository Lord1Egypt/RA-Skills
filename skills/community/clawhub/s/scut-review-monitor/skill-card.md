## Description:

Check or monitor the SCUT thesis blind-review status page through the graduate portal and refresh cookies through a local Python helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Students or their local agents use this skill to check the current SCUT thesis blind-review status, refresh portal login cookies, and monitor the watched status field for changes when continuous monitoring is explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login flow uploads live login QR codes to a configured third-party image host by default.

Mitigation: Disable image_upload.enabled unless remote QR-code sharing is explicitly needed, use only an approved host, and delete generated QR URL and upload-response files after use.

Risk: The helper stores session cookies and QR-code artifacts on disk.

Mitigation: Treat cookies and QR artifacts as temporary credentials, run the skill in a restricted local environment, limit file access, and remove saved artifacts when they are no longer needed.

Risk: Notification settings can include private targets or keys.

Mitigation: Do not echo notification secrets in chat or logs, and review config.json before execution.

Risk: The helper depends on local Python packages and Playwright Chromium to access a live university portal.

Mitigation: Pin and review dependencies before installation, run one-time checks before continuous monitoring, and stop monitoring when the user no longer needs it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songxf1024/skills/scut-review-monitor)
- [Publisher profile](https://clawhub.ai/user/songxf1024)
- [SCUT graduate portal](https://yjsjw-443.webvpn.scut.edu.cn/)
- [Configured image upload API](https://img.scdn.io/api/v1.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report watched portal text, login-cookie status, QR-code file locations, uploaded QR-code URL location, and old/new status values when monitoring detects a change.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
