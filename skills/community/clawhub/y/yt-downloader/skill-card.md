## Description: <br>
Downloads YouTube videos as high-quality MP4 files and registers them as local assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honeybee1130](https://clawhub.ai/user/honeybee1130) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and developers use this skill when they want an agent to save a YouTube, youtu.be, or Shorts URL as a labeled MP4 asset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local downloader can consume significant disk space when saving high-quality videos. <br>
Mitigation: Confirm the requested download and monitor the OpenClaw assets video directory for storage growth. <br>
Risk: The asset registry records downloaded URLs, labels, file paths, timestamps, and file sizes. <br>
Mitigation: Treat the registry as a local activity log and avoid sensitive labels or URLs when possible. <br>
Risk: Downloads depend on yt-dlp and may fail for private, deleted, live, or age-restricted videos. <br>
Mitigation: Check script output for failures and only retry when the source video is accessible for the intended use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime output includes MP4 files and a JSON asset registry entry.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp for downloading and jq for registry updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
