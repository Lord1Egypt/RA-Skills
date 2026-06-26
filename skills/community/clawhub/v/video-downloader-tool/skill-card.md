## Description: <br>
Universal video downloader supporting multiple platforms including Douyin, Bilibili, YouTube, and TikTok, with URL downloads and Douyin keyword search. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[wwkGit](https://clawhub.ai/user/wwkGit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to download videos from supported video platforms by URL, batch URL list, or Douyin keyword search. It is best suited for controlled personal or evaluation workflows where the user has permission to download the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser mode can use authenticated browser state and runs Chromium with reduced sandboxing. <br>
Mitigation: Use a separate browser profile with only the needed account logged in, prefer a virtual environment, specify an output directory, and avoid browser mode on untrusted sites. <br>
Risk: The skill depends on third-party downloader and browser automation packages that perform network downloads. <br>
Mitigation: Review the dependencies before installation, install them in an isolated environment, and run the downloader only for trusted URLs. <br>
Risk: Downloaded videos may be subject to copyright or platform terms of service. <br>
Mitigation: Download only content that the user has permission to use and follow the relevant platform rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwkGit/video-downloader-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON metadata, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; video files and JSON metadata when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped output directories, per-video metadata JSON, and batch summary JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
