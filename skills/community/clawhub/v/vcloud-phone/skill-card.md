## Description: <br>
Guides an agent through operating the Volcano Engine cloud phone administration platform, including opening the console, searching by instance ID, viewing instance details, and initiating file downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjing0819](https://clawhub.ai/user/wangjing0819) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized operations staff use this skill to navigate a production cloud-phone admin console, locate instances by ID, inspect instance details, and initiate specific file downloads such as logcat logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production admin console actions could target the wrong cloud-phone instance. <br>
Mitigation: Confirm the exact instance ID and intended action with the user before searching, opening details, or starting a download. <br>
Risk: Downloaded instance files may contain credentials, private application data, or other sensitive content. <br>
Mitigation: Avoid downloading credential or private data paths, review and redact files before placing them in the workspace, and delete copied logs when no longer needed. <br>
Risk: File download behavior depends on browser and operating-system download prompts that the agent may not be able to automate. <br>
Mitigation: Ask the user to complete manual download steps, copy only the intended file into the workspace, and confirm the filename before reading it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjing0819/vcloud-phone) <br>
- [Volcano Engine cloud phone admin console](https://vcloud-admin.bytedance.net/vephone/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown or conversational text with step-by-step browser actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the user to manually complete browser download steps and place downloaded files in the workspace before reading them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
