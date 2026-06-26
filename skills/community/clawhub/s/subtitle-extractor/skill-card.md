## Description: <br>
Subtitle extractor for Bilibili, YouTube, Xiaohongshu, Douyin, and local files. Extracts native subtitles or Whisper transcription in original format. Agent handles dependency checking, file naming, and content analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poltawa](https://clawhub.ai/user/poltawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract subtitles or transcribe audio from supported video platforms and local media, then save the resulting subtitle file for downstream summarization, translation, analysis, or Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use platform cookies for Bilibili, Xiaohongshu, or Douyin workflows. <br>
Mitigation: Use narrowly scoped cookie exports, place them only where the workflow requires them, and re-export or remove them after use when handling sensitive accounts. <br>
Risk: The skill may download media, audio, subtitle files, and Whisper model files to local storage. <br>
Mitigation: Run it only on media you are comfortable processing locally and clear temporary audio, subtitle, and model artifacts after sensitive jobs. <br>
Risk: Whisper transcription can process private local media and generate text transcripts that may contain sensitive content. <br>
Mitigation: Avoid private local files unless necessary and review saved transcript locations before sharing outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poltawa/subtitle-extractor) <br>
- [ffmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Cookie Editor](https://cookieeditor.org/) <br>
- [ModelScope faster-whisper base files](https://modelscope.cn/models/pkufool/faster-whisper-base/files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the extraction script, saved subtitle files, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces subtitle file paths plus video metadata; generated subtitle files are SRT or VTT.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
