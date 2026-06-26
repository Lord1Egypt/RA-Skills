## Description: <br>
Uploads and schedules YouTube video content through the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations users use this skill to prepare API requests for uploading, scheduling, and publishing YouTube videos through Publora. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publora API keys or upload URLs could be exposed while preparing API requests. <br>
Mitigation: Keep API keys private, avoid pasting secrets into shared logs or public prompts, and replace example credentials before use. <br>
Risk: The agent can help prepare uploads for sensitive, unreleased, or unintended video content. <br>
Mitigation: Verify the video file, channel ID, title, description, scheduled time, and privacy setting before uploading or publishing. <br>
Risk: YouTube uploads may publish publicly by default if privacy settings are not reviewed. <br>
Mitigation: Confirm whether the intended privacy setting is public, unlisted, or private before scheduling the post. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/publora-youtube) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post) <br>
- [Publora get-upload-url endpoint](https://api.publora.com/api/v1/get-upload-url) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with JavaScript and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes YouTube platform limits, Publora request fields, upload flow, privacy settings, and scheduling notes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, released 2026-03-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
