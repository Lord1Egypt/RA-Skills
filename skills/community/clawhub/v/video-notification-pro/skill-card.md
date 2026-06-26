## Description: <br>
Sends an IVVR video notification to a specified mobile phone number using a local video file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhu-xiao-di](https://clawhub.ai/user/zhu-xiao-di) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators use this skill to upload a local video file to an IVVR service and initiate a video notification call to an 11-digit mobile phone number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each invocation can upload the selected local video and recipient phone number to an external IVVR endpoint. <br>
Mitigation: Use only a trusted IVVR endpoint and credentials, and confirm the selected video path and recipient before execution. <br>
Risk: HTTPS certificate verification is disabled in the artifact behavior. <br>
Mitigation: Require the publisher to remove verify=False or configure a trusted certificate authority before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhu-xiao-di/video-notification-pro) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls] <br>
**Output Format:** [JSON status object with success, message, and file_id/task_id fields when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads local video files up to 5 MB and sends one recipient phone number per invocation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
