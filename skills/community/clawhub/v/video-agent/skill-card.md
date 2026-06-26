## Description: <br>
Deprecated HeyGen skill that helps an agent generate, manage, and retrieve AI avatar videos while directing users toward the newer create-video and avatar-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelwang11394](https://clawhub.ai/user/michaelwang11394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to create talking-head videos, explainers, and presentations through HeyGen MCP tools or HeyGen API calls. It is mainly useful for backward compatibility with older HeyGen workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated and documents older HeyGen v1/v2 endpoints. <br>
Mitigation: Prefer the newer create-video or avatar-video skills when possible; use this release only for legacy compatibility. <br>
Risk: The skill can use a HeyGen API key to send selected media, prompts, portraits, and customer data to HeyGen. <br>
Mitigation: Review uploads, prompts, portraits, and customer data before use, and grant HeyGen API access only in environments where that data sharing is acceptable. <br>
Risk: Webhook URLs and delete actions can affect real workflows or assets. <br>
Mitigation: Review webhook URLs and destructive actions before execution, and verify webhook signatures in real deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelwang11394/video-agent) <br>
- [HeyGen Video Agent API](https://docs.heygen.com/reference/generate-video-agent) <br>
- [Authentication reference](references/authentication.md) <br>
- [Video Agent reference](references/video-agent.md) <br>
- [Video generation reference](references/video-generation.md) <br>
- [Video status reference](references/video-status.md) <br>
- [Webhook reference](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code snippets, HTTP examples, and MCP tool-call recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEYGEN_API_KEY or connected HeyGen MCP tools; outputs may include request configurations, video IDs, polling guidance, and download URLs.] <br>

## Skill Version(s): <br>
2.23.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
