## Description: <br>
ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径，并覆盖从快速信息梳理、系统分析到超万字专家报告的全流程，用于企业分析、市场洞察、招商研究等复杂任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhushanwei](https://clawhub.ai/user/zhushanwei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External researchers, business analysts, and agents use this skill to submit research prompts to ZeeLin, choose deep or expert research modes, poll for completion, and retrieve generated reports. It supports market research, company analysis, policy review, technical comparisons, and other decision-support research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and generated reports are sent to ZeeLin's external service. <br>
Mitigation: Use the skill only for content that may be shared with ZeeLin, and avoid submitting confidential or regulated information unless that external processing is approved. <br>
Risk: Generated reports may be written to temporary local files or Feishu documents. <br>
Mitigation: Confirm the delivery channel before use, restrict report sharing to intended recipients, and clean up temporary report files when the environment retains /tmp contents. <br>
Risk: The skill requires a DESEARCH_API_KEY for authenticated API calls. <br>
Mitigation: Store the API key in the environment, rotate it if exposed, and avoid embedding it in prompts, logs, or shared scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhushanwei/zeelin-deep-research) <br>
- [ZeeLin Deep Research Service](https://desearch.zeelin.cn) <br>
- [ZeeLin API Key and Activity Page](https://desearch.zeelin.cn/skill-activity) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; runtime workflows retrieve generated report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a DESEARCH_API_KEY; generated report delivery depends on the external ZeeLin service and selected channel workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
