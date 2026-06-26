## Description: <br>
ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhushanwei](https://clawhub.ai/user/zhushanwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit research prompts to ZeeLin, choose a deep or major research mode, and receive a completed PDF research report link through their configured message channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts, task titles, and generated report links are sent to ZeeLin and to the configured message channel. <br>
Mitigation: Install only if you trust ZeeLin and the configured channel; use a limited ZeeLin API key where possible and confirm target_user/channel before running. <br>
Risk: Generated research reports may be used for business, market, policy, technical, or investment decisions. <br>
Mitigation: Review the PDF report and source assumptions before relying on it for decisions or sharing it outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhushanwei/zeelin-deep-research-pro) <br>
- [ZeeLin API key console](https://skills.zeelin.cn/console/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown instructions with shell commands and message text containing a PDF report link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, a ZeeLin API key, and a configured target message channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
