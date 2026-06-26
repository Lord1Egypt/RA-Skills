## Description: <br>
Download YouTube video audio and convert it to MP3, with optional cookies for age-restricted videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to download YouTube audio as MP3 output for a larger translation workflow. It can pass a cookies file when the source video requires authenticated access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured tool entry points to an absolute Python file outside the reviewed artifact. <br>
Mitigation: Review the external download_audio.py before use, or ask the publisher to include the downloader in the package with a package-relative entry path. <br>
Risk: A cookies.txt file may contain sensitive authenticated session data. <br>
Mitigation: Provide cookies only when necessary, keep the file out of shared storage and version control, and remove it when no longer needed. <br>


## Reference(s): <br>
- [Youtube Audio Download on ClawHub](https://clawhub.ai/banner90/youtube-audio-download) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON status object with an MP3 audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional cookies path and output directory parameters; expected execution is a Windows Python call from WSL.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
