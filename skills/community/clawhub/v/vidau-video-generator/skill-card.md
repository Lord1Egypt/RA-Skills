## Description: <br>
Use Vidau Open API to generate short videos with Veo3, Sora2, and other models, or query account credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigjoehuang](https://clawhub.ai/user/bigjoehuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill through an agent to generate short videos from prompts or uploaded media, check Vidau credits, and monitor video task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Vidau API key. <br>
Mitigation: Install only when the Vidau API key can be granted to the agent, keep the key in the configured environment or OpenClaw entry, and rotate it if exposed. <br>
Risk: The skill can upload selected local image or video files to Vidau asset storage. <br>
Mitigation: Confirm the user intends to upload each local media file and avoid sending private or sensitive media unless that transfer is acceptable. <br>
Risk: The artifact includes automatic Python installation guidance that may modify the host setup. <br>
Mitigation: Review or remove automatic package installation steps before deployment, and require operator approval for host-level installs. <br>
Risk: API requests and responses may be logged locally in ~/vidau_api.log, including prompts, task identifiers, account responses, and generated media links. <br>
Mitigation: Set VIDAU_API_LOG to a managed location, disable or periodically delete the log where possible, and treat the log as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigjoehuang/vidau-video-generator) <br>
- [Vidau Open API documentation](https://doc.superaiglobal.com/en/overview/introduction) <br>
- [Vidau homepage](https://vidau.ai) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [Model reference](references/models.md) <br>
- [Parameter reference](references/parameters.md) <br>
- [Error handling reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown responses with code blocks for generated video and thumbnail URLs; helper scripts return JSON for credits, model capabilities, task creation, uploads, and task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIDAU_API_KEY; may upload selected local media to Vidau and uses local cache or log files.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
