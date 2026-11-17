## Description: <br>
A lightweight video upload skill that helps an agent upload a local video to a streaming service and return an HLS playback link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users can use this skill to upload one local video with a title, authenticate to a streaming API, trigger transcoding, and receive a playback link. It is best suited to small single-video uploads, teaching videos, personal content sharing, and basic video backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local videos to a third-party streaming service where they may become publicly accessible. <br>
Mitigation: Confirm the exact file path, title, destination account, and intended public visibility before running upload commands. <br>
Risk: The upload flow uses stream public and secret keys in shell commands and API headers. <br>
Mitigation: Provide secrets through protected environment variables or a secure prompt, and avoid pasting secret keys into terminal history, shared logs, or transcripts. <br>
Risk: The free workflow is limited to single-video, single-part uploads and may fail or time out for larger files. <br>
Mitigation: Use small files consistent with the artifact guidance, verify completion status after upload, and choose a more capable workflow for batch or large-file uploads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/video-stream-upload-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Streaming API base URL](https://api-w3stream.attoaioz.cyou) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns upload status, transcoding status, and HLS or DASH playback links when the streaming API succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
