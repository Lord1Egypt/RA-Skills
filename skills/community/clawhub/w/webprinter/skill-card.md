## Description:

调用官方 WebPrinter 云打印服务（webprinter.cn），提供企业智慧文印、打印管控、共享打印、远程打印等全套打印管理功能，包括查询打印机、上传本地文件、创建漫游打印任务、直接打印到指定设备，以及更新单双面、颜色、份数和纸张等打印参数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimsoft](https://clawhub.ai/user/zimsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business users use this skill to work with WebPrinter cloud printing: checking printer availability, uploading local files, creating roaming print jobs, direct-printing to selected devices, and adjusting print settings for existing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Print actions may send documents or document URLs to an external WebPrinter cloud service.

Mitigation: Use the skill only with documents approved for this cloud printing flow and confirm the exact local file or HTTPS URL before submission.

Risk: The skill can create real print jobs through roaming print or direct print actions.

Mitigation: Confirm the intended destination printer or roaming queue and print settings before executing print commands.

Risk: The WebPrinter bearer token grants access to cloud printing actions for the configured account.

Mitigation: Store WEBPRINTER_ACCESS_TOKEN only in the runtime environment and install the skill only where WebPrinter and its token handling are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimsoft/skills/webprinter)
- [WebPrinter service](https://any.webprinter.cn)
- [WebPrinter OAuth token page](https://any.webprinter.cn/get-ai-server-token)
- [WebPrinter setup document](https://liqdopokb8.feishu.cn/docx/A0audnVIaoolXqxWUHPcvl1UnFd)
- [Cloud Driver Print reference](https://github.com/zimsoft/cloud-driver-print/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WEBPRINTER_ACCESS_TOKEN and a WebPrinter client/device setup before print actions.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
