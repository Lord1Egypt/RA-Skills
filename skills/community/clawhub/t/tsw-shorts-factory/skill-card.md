## Description: <br>
Autonomous YouTube Shorts video factory that generates quote-based short-form videos using edge-tts, Pexels stock footage, and MoviePy local assembly, then prepares YouTube uploads for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vanyanski](https://clawhub.ai/user/Vanyanski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to set up a local automation pipeline for generating quote-based vertical Shorts, caching stock clips, creating voiceover audio, assembling MP4 files, and uploading draft or unlisted videos to YouTube for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged code includes under-disclosed account-upload behavior and can run unattended uploads when scheduled. <br>
Mitigation: Review the upload path before enabling cron, keep uploads private or unlisted until approved, and require a human review step before publishing. <br>
Risk: The packaged code uses hard-coded local paths and an embedded Pexels API key. <br>
Mitigation: Replace hard-coded paths and credentials with user-controlled configuration before installation or execution. <br>
Risk: The security evidence notes a missing YouTube uploader implementation and a stored OAuth token path. <br>
Mitigation: Audit any uploader implementation before use and protect or remove the OAuth token file when not actively needed. <br>


## Reference(s): <br>
- [YouTube OAuth Setup](references/youtube-setup.md) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/Vanyanski/tsw-shorts-factory) <br>
- [Publisher Profile](https://clawhub.ai/user/Vanyanski) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for local video generation and upload automation; the packaged scripts produce MP4 video files and YouTube upload attempts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
