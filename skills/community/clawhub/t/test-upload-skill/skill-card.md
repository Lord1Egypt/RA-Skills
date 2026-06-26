## Description: <br>
A simple test skill for verifying clawhub.ai upload functionality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoshitou1](https://clawhub.ai/user/xiaoshitou1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub publishers use this skill to verify that a skill upload can load, respond with a status message, and report a timestamp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill does not provide useful production functionality beyond upload and loading verification. <br>
Mitigation: Use it only as a platform loading test, not as a production workflow dependency. <br>
Risk: A successful status message may be mistaken for a broader validation of the hosting platform or agent runtime. <br>
Mitigation: Treat the response as confirmation that this skill loaded and responded; run separate checks for platform, metadata, and trigger behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoshitou1/test-upload-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Plain text status message in a Markdown-compatible response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a current ISO timestamp and basic operational status text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
