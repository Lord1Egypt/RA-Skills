## Description: <br>
Video Crawler helps an agent download videos from Douyin or Twitter/X when given a supported platform, URL, and optional output file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators can use this skill to fetch video files from supported social platforms for workflows where they are authorized to download the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a hardcoded API key unrelated to the stated video download behavior. <br>
Mitigation: Remove the key before use and rotate it if it is real. <br>
Risk: Downloaded files can be written to an arbitrary user-supplied output path. <br>
Mitigation: Run the skill with a dedicated download directory and avoid system or configuration paths. <br>
Risk: The skill can download third-party platform content. <br>
Mitigation: Use it only for videos the operator owns or is authorized to download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ly5201314gjx/video-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Command-line text output and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [On success the script prints the saved file path; on failure it prints an error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
