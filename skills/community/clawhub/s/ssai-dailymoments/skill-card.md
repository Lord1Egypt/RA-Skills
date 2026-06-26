## Description: <br>
ssai-dailymoments helps Squirrel AI study-room operators generate five WeChat Moments posts with warm education-themed copy and hand-drawn-style illustrations, either manually or on a daily schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keystone-shiqi](https://clawhub.ai/user/keystone-shiqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External education-center operators use this skill to create parent-facing WeChat Moments marketing content with matching portrait illustrations. It supports manual generation on request and scheduled daily content generation for recurring social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image-generation prompts to a MiniMax-compatible image API and may incur provider costs or expose prompt content to that provider. <br>
Mitigation: Configure only a trusted image provider and valid API key, and review provider data-handling and billing terms before enabling the skill. <br>
Risk: Scheduled generation can create recurring marketing content without a fresh manual request each time. <br>
Mitigation: Enable scheduled runs only for intended accounts and review initial outputs before using them in customer-facing channels. <br>
Risk: The skill keeps a local history file to avoid repeated posts. <br>
Mitigation: Manage or delete the local history file according to the operator's retention and privacy expectations. <br>


## Reference(s): <br>
- [MiniMax image generation API](https://api.minimaxi.com/v1/image_generation) <br>
- [ClawHub skill page](https://clawhub.ai/keystone-shiqi/ssai-dailymoments) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, API calls, Configuration guidance] <br>
**Output Format:** [Plain text paired with generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates five WeChat Moments posts with matching portrait 3:4 illustrations and keeps local history to reduce repeated content.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
