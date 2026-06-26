## Description: <br>
This skill helps an agent batch download QR code invitation images from XingTu recruitment tasks by validating cookie authentication, fetching task lists through the XingTu API, opening each task detail page, and saving invitation QR images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanjuan2538](https://clawhub.ai/user/juanjuan2538) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operations teams use this skill to automate downloading QR code invitation images for active XingTu recruitment tasks. It is intended for authenticated XingTu account workflows where the user approves credential use, browser automation, and the local output location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores and reuses live XingTu login cookies in plain text. <br>
Mitigation: Treat ~/.xingtuCookie.txt as password-equivalent, avoid pasting cookies into chat unless necessary, and delete or rotate the cookie after use. <br>
Risk: The skill can run long browser automation and batch download work using an authenticated XingTu session. <br>
Mitigation: Review and approve the batch run, task scope, and output directory before execution, and monitor progress for unexpected behavior. <br>
Risk: Authentication failures, expired cookies, or zero-participant tasks can interrupt the workflow. <br>
Mitigation: Validate cookies before API calls, resume from the JSON progress file, and skip tasks that cannot open the invitation modal. <br>


## Reference(s): <br>
- [XingTu API Reference](references/api_spec.md) <br>
- [XingTu task list API](https://www.xingtu.cn/gw/api/task/provider_get_task_order_list) <br>
- [XingTu login](https://sso.oceanengine.com/xingtu/login?role=7) <br>
- [ClawHub skill page](https://clawhub.ai/juanjuan2538/xingtu-task-invite-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with PowerShell, Python, browser automation commands, JSON progress data, and downloaded PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local cookie, task-cache, progress, download, and output paths during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
