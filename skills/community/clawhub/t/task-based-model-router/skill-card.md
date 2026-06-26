## Description: <br>
Optimize Your API Costs - Route tasks to cost-effective models via TokenRouter. Dynamically builds model tiers from live pricing, classifies tasks into 6 categories (supporting English & Chinese), and orchestrates multi-agent workflows with adaptive fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yb98k999](https://clawhub.ai/user/yb98k999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a PaleBlueDot AI TokenRouter provider, compare live model pricing, and generate task-specific routing plans for coding, analysis, writing, creative, translation, and simple tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user-provided TokenRouter credentials and modify global OpenClaw model configuration. <br>
Mitigation: Review ~/.openclaw/openclaw.json before and after setup, keep backups under user control, and use a limited-scope API key when available. <br>
Risk: The skill can change allowed models and routing behavior for the user's OpenClaw environment. <br>
Mitigation: Inspect synced and enabled model changes before relying on generated routing plans, especially in shared or production workspaces. <br>
Risk: The included local file-inspection tools can read broad workspace content. <br>
Mitigation: Run smart_find.py and smart_map.py only on workspaces where broad local file inspection is intended and appropriate. <br>


## Reference(s): <br>
- [Smart Model Router on ClawHub](https://clawhub.ai/yb98k999/task-based-model-router) <br>
- [PaleBlueDot AI](https://www.palebluedot.ai) <br>
- [TokenRouter API base URL](https://open.palebluedot.ai/v1) <br>
- [TokenRouter pricing API](https://www.palebluedot.ai/openIntelligence/api/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON execution plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw configuration and produce routing plan files when the user chooses setup, sync, enable, or execution planning flows.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
