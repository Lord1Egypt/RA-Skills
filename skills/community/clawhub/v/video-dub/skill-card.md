## Description: <br>
Windows-first video localization pipeline for downloading, transcribing, translating, dubbing, and retiming YouTube or Bilibili videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bzxcup-afk](https://clawhub.ai/user/bzxcup-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video localization operators use this skill to run a local pipeline that turns YouTube or Bilibili source videos into dubbed videos with aligned subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DeepSeek API key and can optionally use a YouTube cookies file. <br>
Mitigation: Provide credentials through the current shell or a controlled secret store, avoid echoing secrets, and avoid persistent user-level secrets on shared machines. <br>
Risk: Video-derived transcript and subtitle text may be sent to DeepSeek and the selected TTS provider. <br>
Mitigation: Do not process private, regulated, or copyrighted media unless provider terms and local artifact storage are acceptable. <br>
Risk: Video processing creates local intermediate media, audio, subtitle, and debug files. <br>
Mitigation: Run the pipeline in a workspace with adequate disk space and remove generated artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/bzxcup-afk/video-dub) <br>
- [Video Pipeline README](video_pipeline/README.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Release Bundle Layout](references/release_bundle.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with file paths and PowerShell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paths to dubbed video files, aligned SRT subtitle files, and optional intermediate JSON or debug files.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
