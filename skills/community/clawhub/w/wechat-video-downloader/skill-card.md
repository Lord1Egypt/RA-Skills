## Description: <br>
Extracts embedded video URLs from WeChat official account articles and downloads the videos locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenjie0112](https://clawhub.ai/user/wenjie0112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve videos from WeChat official account articles when they provide an article URL and are authorized to save the content locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-provided WeChat article links, extracts media URLs, and saves files locally. <br>
Mitigation: Use it only with trusted article URLs and content the user is authorized to download. <br>
Risk: Ambiguous download requests can cause files to be saved in unintended names or directories. <br>
Mitigation: Confirm unclear requests and choose safe output filenames and directories before running the download. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wenjie0112/wechat-video-downloader) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads video files to a user-selected or generated local filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
