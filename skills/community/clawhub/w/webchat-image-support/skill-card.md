## Description: <br>
Enables agents to detect and analyze images sent via WebChat or other channels using vision-capable models or fallback media processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[styoha](https://clawhub.ai/user/styoha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let OpenClaw agents understand image attachments across WebChat and other chat channels. It is useful for screenshot analysis, photo interpretation, and multi-image messages when a configured model or fallback media pipeline supports vision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images sent to the agent may be processed by configured vision providers or OpenClaw media services. <br>
Mitigation: Avoid uploading private screenshots, documents, faces, or regulated data unless the provider and retention settings are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/styoha/webchat-image-support) <br>
- [OpenClaw documentation](https://openclaw.dev) <br>
- [OpenClaw gateway issue #57064](https://github.com/openclaw/openclaw/issues/57064) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill behavior depends on the configured vision-capable model or OpenClaw media pipeline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
