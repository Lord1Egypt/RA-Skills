## Description: <br>
Guides an agent to find existing Tokenrouter channel configuration, add missing video model routes with minimal config changes, and create and poll video generation tasks through Tokenrouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yb98k999](https://clawhub.ai/user/yb98k999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare a workspace's Tokenrouter configuration for supported video models and run text-to-video or image-to-video generation through an existing Tokenrouter channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Tokenrouter routing edits may change workspace behavior or disrupt the running service. <br>
Mitigation: Review the proposed config diff before applying it, keep edits scoped to the requested model route, and run the workspace's reload or validation command when available. <br>
Risk: Video generation requests can use an existing Tokenrouter key and consume paid quota. <br>
Mitigation: Confirm the configured key belongs to the intended account and that the user approves the paid API request before submitting generation jobs. <br>
Risk: Prompts and image URLs are sent to Tokenrouter and potentially upstream video providers. <br>
Mitigation: Avoid submitting sensitive prompts, private images, or confidential media unless the user has approved sending that data to the service. <br>


## Reference(s): <br>
- [Tokenrouter Video API Reference](artifact/references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/yb98k999/tokenrouter-generate-video) <br>
- [Tokenrouter registration](https://www.tokenrouter.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect and edit local Tokenrouter configuration, reload services, and submit video-generation API requests using an existing configured key.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
