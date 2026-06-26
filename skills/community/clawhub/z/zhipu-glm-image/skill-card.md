## Description: <br>
Generates and downloads images through the Zhipu GLM-Image web interface using an existing browser login session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangm199](https://clawhub.ai/user/huangm199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check Zhipu Image login readiness, open the web login flow when needed, submit image-generation prompts, and save generated PNG files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles browser login cookies and stores them in a local session file. <br>
Mitigation: Use a dedicated browser profile when possible, treat the session file like a password, and delete it when the skill is no longer needed or if exposure is suspected. <br>
Risk: The network monitor can observe request details from the browser debugging session. <br>
Mitigation: Run the monitor only when troubleshooting this skill and avoid browsing unrelated sites while it is active. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/huangm199/zhipu-glm-image) <br>
- [Zhipu Image web app](https://image.z.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts print JSON status and generation results and save PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local browser session file and downloads generated images into a captures directory by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
