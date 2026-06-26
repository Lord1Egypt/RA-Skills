## Description: <br>
Star Office UI 一键部署技能 — 帮主人快速部署像素办公室看板，支持多 Agent 加入、状态可视化、移动端查看与公网访问 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiustrator](https://clawhub.ai/user/iiustrator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to deploy a local pixel-office dashboard for viewing multiple agents, status changes, yesterday notes, custom art assets, and optional Gemini-backed image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes public tunnel guidance while the dashboard sidebar uses a weak default password. <br>
Mitigation: Change ASSET_DRAWER_PASS from 1234 before using a public tunnel or any long-running deployment. <br>
Risk: The dashboard may expose notes, status text, endpoints, or locally configured assets to viewers. <br>
Mitigation: Review visible notes, dashboard endpoints, and asset settings before sharing the local or tunneled URL. <br>
Risk: Optional image generation requires a Gemini API key. <br>
Mitigation: Provide GEMINI_API_KEY only when the image-generation feature is needed, and store it through environment or app configuration appropriate for the deployment. <br>
Risk: Artifact documentation says code can be used under MIT terms but bundled art assets are not for commercial use. <br>
Mitigation: Confirm the final license terms and replace bundled art assets with original or properly licensed assets for commercial deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iiustrator/star-office-deploy) <br>
- [Star Office UI repository referenced by skill instructions](https://github.com/ringhyacinth/Star-Office-UI.git) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment steps, status-change examples, optional Gemini API setup, tunnel guidance, and security reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
