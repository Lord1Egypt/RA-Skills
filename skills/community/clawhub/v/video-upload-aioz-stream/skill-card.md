## Description: <br>
Quick upload video to AIOZ Stream API. Create video objects with default or custom encoding configurations, upload the file, complete the upload, then return the video link to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhbui3004](https://clawhub.ai/user/vinhbui3004) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create AIOZ Stream video records, upload local video files, finalize transcoding, and retrieve streaming links. It also supports optional cost estimation, thumbnail upload, and custom encoding configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AIOZ/W3Stream API credentials may allow broader account actions than video upload. <br>
Mitigation: Use least-privilege or temporary credentials when available, and review the requested action before sharing keys with the agent. <br>
Risk: Secrets passed through shell commands can be exposed in terminal history, logs, or process listings. <br>
Mitigation: Avoid placing public and secret keys directly in logged commands; provide them through a secure runtime path and keep command output private. <br>
Risk: The artifact includes actions that can list, update, replace thumbnails for, or delete existing videos. <br>
Mitigation: Require explicit user confirmation before running any account-wide, metadata-changing, thumbnail replacement, or deletion operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vinhbui3004/video-upload-aioz-stream) <br>
- [AIOZ Stream API endpoint](https://api-w3stream.attoaioz.cyou) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, md5sum, AIOZ Stream API credentials, and access to the local video or thumbnail files being uploaded.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
