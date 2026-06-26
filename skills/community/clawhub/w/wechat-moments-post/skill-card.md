## Description: <br>
Automate posting to WeChat Moments on Windows desktop by opening the Moments window, triggering the publish entry, selecting an image, pasting a caption, clicking publish, and checking the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zch-danny](https://clawhub.ai/user/zch-danny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation operators use this skill to publish an image and caption to WeChat Moments from a Windows desktop session. It is intended for workflows where the account, target image, caption, and publish action have already been intentionally chosen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can publish directly to a live WeChat Moments account without a final confirmation step. <br>
Mitigation: Run it only when the account, image path, caption, and intended audience have been verified, and prefer adding or enforcing a manual confirmation before the Publish click. <br>
Risk: The configured WeChat executable path could point to an unintended program. <br>
Mitigation: Review WECHAT_EXE before execution and confirm it points to the real WeChat desktop executable. <br>
Risk: Temporary screenshots used for OCR verification can contain account or desktop content. <br>
Mitigation: Keep sensitive windows closed while running the skill and delete the temporary screenshot directory after use. <br>


## Reference(s): <br>
- [WeChat Moments workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/zch-danny/wechat-moments-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python script references and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces desktop automation steps that may operate a live WeChat session and write temporary screenshots for verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
