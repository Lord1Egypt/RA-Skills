## Description: <br>
Complete toolkit for publishing content to Xiaohongshu (小红书), including automated browser control, image generation, content formatting, and a publishing pipeline for OpenClaw browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siaslfs](https://clawhub.ai/user/siaslfs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare Xiaohongshu posts, generate cover images, maintain an OpenClaw browser login session, and publish image-text notes through the Xiaohongshu creator platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content automatically to a real Xiaohongshu account. <br>
Mitigation: Add a manual preview or confirmation step before any post goes live, and use a test or low-risk account when evaluating the workflow. <br>
Risk: The skill preserves and refreshes browser login sessions for unattended operation. <br>
Mitigation: Use a dedicated OpenClaw browser profile and avoid cron or daemon keepalive unless unattended operation is explicitly required. <br>
Risk: The security evidence notes unsafe shell-built commands when titles, content, or paths are passed into scripts. <br>
Mitigation: Do not pass untrusted titles, content, or file paths into the scripts without validation and quoting controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/siaslfs/xiaohongshu-publish-kit) <br>
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com) <br>
- [Xiaohongshu publish page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces publishing commands, Python automation examples, browser setup guidance, and configuration steps for OpenClaw-managed Xiaohongshu workflows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
