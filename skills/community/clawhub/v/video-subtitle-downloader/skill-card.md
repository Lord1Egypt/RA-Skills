## Description: <br>
Downloads and converts subtitles from supported video platforms into SRT, JSON, or TXT files using yt-dlp, with optional batch processing and documented GPU transcription support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to fetch subtitles or transcript-like text from videos they are permitted to process, then export them for notes, translation, review, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses external video URLs and invokes yt-dlp, so normal use may fetch content from third-party platforms. <br>
Mitigation: Install it in a virtual environment, test one URL before batch mode, and review yt-dlp options before running. <br>
Risk: Subtitle download or transcription can process copyrighted, private, or otherwise restricted videos. <br>
Mitigation: Only process videos the user has rights or permission to download or transcribe. <br>
Risk: Batch mode can process many URLs and write multiple local subtitle files. <br>
Mitigation: Use a dedicated output folder and inspect URL lists before batch processing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shenghoo123-png/video-subtitle-downloader) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands and subtitle files in SRT, JSON, or TXT format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes files under a user-selected output directory; batch mode reads a URL list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
