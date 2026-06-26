## Description: <br>
Sends local images to Feishu group or individual chats using Feishu app credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ye1358215818](https://clawhub.ai/user/ye1358215818) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send screenshots, design images, and other local image files to Feishu groups or individual recipients from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret or access credentials could be exposed if pasted into chat, code, or logs. <br>
Mitigation: Keep credentials in environment variables or a secret manager, avoid sharing them in prompts, and rotate any credentials that may have been exposed. <br>
Risk: The skill can send images through a Feishu app, so an incorrect recipient ID or overbroad app permission can send content to the wrong place. <br>
Mitigation: Use a least-privilege Feishu app and confirm the image path and chat or user ID before each send. <br>
Risk: The JavaScript helper imports a parent-relative Feishu media module that is not included in the artifact. <br>
Mitigation: Verify the referenced helper dependency before use, or remove the JavaScript helper and rely on the reviewed Python path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ye1358215818/zoe-feishu-media) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime calls return Feishu API JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a local image path, and a Feishu chat or user ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
