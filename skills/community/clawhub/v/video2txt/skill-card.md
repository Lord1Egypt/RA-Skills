## Description: <br>
Extract transcripts and subtitles from video URLs, optionally translate non-Chinese transcripts into Chinese, and deliver the result as DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vistalyq](https://clawhub.ai/user/vistalyq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill when a video URL needs to be converted into a readable transcript or lecture-note style document. It is suited for extracting available subtitles from YouTube, Bilibili, or other yt-dlp supported platforms and producing one or two DOCX files depending on language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs yt-dlp and Node locally, may install the docx npm dependency, fetches subtitles from video platforms, and writes transcript files. <br>
Mitigation: Install only in environments where local command execution and dependency installation are acceptable, use trusted video URLs, and review output paths before sharing generated DOCX files. <br>
Risk: Private, geo-blocked, or subtitle-free videos may not produce usable transcript output. <br>
Mitigation: Confirm the video is accessible and has available subtitles; use a separate speech-recognition workflow when subtitles cannot be extracted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vistalyq/video2txt) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [DOCX transcript files with optional text preview and file-path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local transcript_original.docx and/or transcript_zh.docx files from downloaded subtitles; non-Chinese transcripts may be translated to Chinese.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
