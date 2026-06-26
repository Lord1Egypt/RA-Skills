## Description: <br>
video-transcript helps agents extract available YouTube or Bilibili subtitles and convert them into a plain-text video transcript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TupleYe](https://clawhub.ai/user/TupleYe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill when they need a text transcript from a supported video link that already has subtitles. It is intended for YouTube and Bilibili links and produces transcript text for review, summarization, translation, or note-taking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes yt-dlp against user-provided video URLs and depends on a locally installed executable. <br>
Mitigation: Install yt-dlp only from a trusted source and use the skill only with video links the user intends to process. <br>
Risk: Downloaded subtitles and generated transcript files may contain sensitive or copyrighted content and are stored locally. <br>
Mitigation: Review transcript sensitivity before sharing outputs and delete ~/.openclaw/workspace/video-transcripts when local copies are no longer needed. <br>
Risk: The artifact describes Chinese translation behavior, but the security guidance says not to rely on translation unless a separate translation step is added. <br>
Mitigation: Treat this skill as subtitle extraction and transcript formatting; use a separate translation step when translated output is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TupleYe/videotranscript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown-oriented transcript text with optional shell command usage and a local .txt transcript file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and videos with existing subtitles; local transcript files are written under ~/.openclaw/workspace/video-transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
