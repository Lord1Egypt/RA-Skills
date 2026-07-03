## Description: <br>
Video Remove Background guides agents through Bria API authentication and video background removal to produce transparent, alpha-channel, or solid-color video outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to remove backgrounds from short video files or URLs for compositing, overlays, product content, and batch cutouts through Bria's remote API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive videos are uploaded to Bria for remote processing. <br>
Mitigation: Use only videos that are appropriate to send to Bria, and obtain approval before processing confidential, regulated, or customer-owned footage. <br>
Risk: Reusable Bria credentials may be stored in plaintext at ~/.bria/credentials. <br>
Mitigation: Protect the credentials file, avoid shared machines for sensitive work, and delete or rotate credentials after use when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/galbria/skills/video-remove-background) <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_video_client.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and processed video result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May authenticate with Bria, upload local videos, poll asynchronous video jobs, and return temporary processed-video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.3.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
