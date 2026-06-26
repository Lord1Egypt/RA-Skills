## Description: <br>
Seedance 2.0 helps agents guide users through Volcengine access setup and generate videos from prompts, templates, and reference media through the Ark API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoyi](https://clawhub.ai/user/airoyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review Seedance 2.0 access requirements, configure Ark API credentials, generate videos from prompts or templates, and save the resulting video files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Ark API key and supports a configurable API base URL. <br>
Mitigation: Use a restricted ARK_API_KEY, keep ARK_BASE_URL pointed at a trusted endpoint, and avoid committing credentials to the skill directory. <br>
Risk: Prompts and reference media URLs are sent to an external video-generation service. <br>
Mitigation: Avoid sensitive prompts, private media URLs, and content that should not leave the local environment. <br>
Risk: Generated videos may be downloaded to local disk. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or deploying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airoyi/seedance-2-0) <br>
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, files] <br>
**Output Format:** [Console text, API task responses, and local video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and may use ARK_BASE_URL; generated videos can be downloaded to a local output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
