## Description: <br>
Post or schedule video content to TikTok using the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Publora API calls for creating, uploading, and scheduling TikTok video posts. It is suited for workflows that need TikTok-specific platform limits, upload steps, and common posting error guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps create, upload, and schedule TikTok videos through Publora, so incorrect captions, platform IDs, schedule times, or video files could publish unintended content. <br>
Mitigation: Review the caption, platform ID, schedule time, and selected video before sending API requests or allowing an agent to execute them. <br>
Risk: Publora API keys are required for publishing workflows and could grant posting access if exposed. <br>
Mitigation: Use a scoped Publora API key when available, avoid pasting long-lived secrets into shared logs or prompts, and revoke keys that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sergebulaev/publora-tiktok) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post) <br>
- [Publora upload URL endpoint](https://api.publora.com/api/v1/get-upload-url) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with JavaScript and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Publora request guidance for TikTok video posts; users provide captions, platform IDs, schedule times, and video files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
