## Description: <br>
Download videos from mainstream websites from a user-provided URL and save the media locally for viewing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skill](https://clawhub.ai/user/skill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user provides a video URL and wants the video downloaded into the local workspace for later viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads media from user-provided URLs, which can involve copyright restrictions or site terms of service. <br>
Mitigation: Use it only for URLs the user is authorized to download and review applicable site terms before use. <br>
Risk: Downloaded videos can consume significant disk space in the local workspace. <br>
Mitigation: Run it in a workspace where a local videos directory and large media files are acceptable, then clean up files that are no longer needed. <br>
Risk: Untrusted URLs can lead the agent to fetch unwanted or unsafe content. <br>
Mitigation: Confirm the URL source is trusted before running the download. <br>


## Reference(s): <br>
- [Save Video on ClawHub](https://clawhub.ai/skill/save-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text status message and downloaded video file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local videos directory in the current workspace and writes the downloaded media there.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
