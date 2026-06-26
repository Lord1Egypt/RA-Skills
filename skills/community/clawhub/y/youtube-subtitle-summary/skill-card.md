## Description: <br>
Extracts subtitles from YouTube or Bilibili videos, saves the raw transcript, and generates a structured summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiapuyang](https://clawhub.ai/user/xiapuyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn YouTube or Bilibili videos into cleaned transcript files and structured Markdown summaries. It is useful for reviewing video content, extracting key ideas, and preserving video metadata alongside the generated notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install or update yt-dlp during execution. <br>
Mitigation: Preinstall a trusted yt-dlp version through your normal package-management process and review any update behavior before running the skill. <br>
Risk: Bilibili subtitle access may read browser-derived login cookies and store them in a local cookies file. <br>
Mitigation: Set BILIBILI_COOKIES_FILE to a dedicated restricted path, avoid sharing the file, and delete it after use when persistent access is not needed. <br>
Risk: Raw transcripts and summaries may be written to local Markdown files without a separate consent prompt. <br>
Mitigation: Set YOUTUBE_SUBTITLES_DIR to an approved output directory and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiapuyang/youtube-subtitle-summary) <br>
- [Publisher Profile](https://clawhub.ai/user/xiapuyang) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, cleaned transcript text, structured summary sections, and supporting shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write transcript and summary files to the current directory or to YOUTUBE_SUBTITLES_DIR; summary language can be controlled with YOUTUBE_SUBTITLES_SUMMARY_LANG.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
