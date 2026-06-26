## Description: <br>
Control Ziniao Browser via the local Ziniao bridge by discovering allowed tools with GET /zclaw/tools and invoking them through POST /zclaw/tools/invoke with API-key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziniao-open](https://clawhub.ai/user/ziniao-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to operate Ziniao Browser stores through the local Ziniao bridge, including listing and opening stores, navigating pages, reading content, interacting with elements, taking screenshots, exporting files, and running supported automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the assistant browser-control authority through the local Ziniao bridge. <br>
Mitigation: Install only when the Ziniao bridge is trusted, keep the bridge bound to localhost, and review browser actions before using the skill for sensitive accounts or workflows. <br>
Risk: The skill handles ZCLAW_API_KEY credentials and may store them in ~/.zclaw/config.json. <br>
Mitigation: Prefer an environment variable or secure credential mechanism, protect any config file containing the key, and know how to delete or rotate the key. <br>
Risk: Invalid or hallucinated bridge tool names could cause failed or unintended browser-control requests. <br>
Mitigation: Use GET /zclaw/tools as the authoritative live tool registry before invoking tools, and fall back only to the documented static allowlist when discovery is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziniao-open/ziniao-assistant) <br>
- [Ziniao Ecosystem Center](https://open.ziniao.com/contactUs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, markdown] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-control requests for a local Ziniao bridge and file-download instructions through the bridge.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
