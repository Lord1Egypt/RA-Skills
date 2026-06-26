## Description: <br>
Use when the user wants to generate a video through the superouter, especially the `seedance-2.0-v1` omni-reference workflow with ordered assets, async submission, `taskId` polling, and direct download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningxiaoxiao](https://clawhub.ai/user/ningxiaoxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate videos through the superouter platform API by checking balance, uploading ordered reference assets, submitting asynchronous video generation tasks, polling task status, and returning final download URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the SUPER_KEY credential and uploaded media to superouter.nesports.top over unencrypted HTTP. <br>
Mitigation: Use only with trusted, low-value or test credentials until the service supports HTTPS for credentialed endpoints; rotate any key already used over HTTP. <br>
Risk: The skill uploads user-provided image, video, or audio files to a third-party remote service. <br>
Mitigation: Confirm the user intends to send each file to the publisher-operated service and avoid uploading sensitive media unless the publisher is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningxiaoxiao/superouter-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/ningxiaoxiao) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task IDs, task status, estimated credit costs, and direct video download URLs from the platform.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
