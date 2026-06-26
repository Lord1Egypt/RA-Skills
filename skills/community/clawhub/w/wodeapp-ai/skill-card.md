## Description: <br>
WodeApp AI Engine lets an agent use one WODEAPP_API_KEY to access hosted text, vision, audio, video, page-building, project, workflow, and MCP/REST capabilities through WodeApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diankourenxia](https://clawhub.ai/user/diankourenxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect agents to WodeApp-hosted multimodal generation, page creation, visual workflows, project publishing, and project-scoped MCP tools. It is useful when a user wants one credential and credit pool for text, image, audio, video, workflow, and hosted project operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate broad hosted-project workflows and publish or change project data through WodeApp APIs. <br>
Mitigation: Require explicit user confirmation before publishing projects, deleting or changing project data, or running workflows that trigger external effects. <br>
Risk: Prompts, uploaded media, workflow inputs and outputs, project configurations, and generated URLs are sent to or produced by WodeApp and may include public or semi-public asset URLs. <br>
Mitigation: Avoid confidential uploads and sensitive data unless the user explicitly accepts the WodeApp data path and sharing model. <br>
Risk: The evidence warns that project MCP endpoints may be unauthenticated. <br>
Mitigation: Treat project MCP endpoints as sensitive capabilities; prefer scoped credentials, billing limits, least-privilege project setup, and user confirmation before connecting or invoking tools. <br>
Risk: The skill can send messages or data through Feishu, WeCom, or DingTalk integrations. <br>
Mitigation: Confirm destination, content, and intended audience before sending data to external collaboration systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diankourenxia/wodeapp-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/diankourenxia) <br>
- [WodeApp Homepage](https://wodeapp.ai) <br>
- [WodeApp Skill Source](https://wodeapp.ai/api-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, REST/MCP call patterns, and generated project or media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted project URLs, workflow outputs, generated asset URLs, and structured JSON responses from WodeApp APIs.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata; artifact frontmatter reports 2.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
