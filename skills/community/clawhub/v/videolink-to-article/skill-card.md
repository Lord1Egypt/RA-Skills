## Description: <br>
Use when the user provides a Bilibili or YouTube URL and asks for a transcript, article, or subtitle extraction. Downloads platform subtitles via BBDown / yt-dlp and produces a clean Markdown transcript in the source language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hqwqf](https://clawhub.ai/user/hqwqf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Bilibili or YouTube video subtitles into clean source-language Markdown transcripts or article-style notes. It is intended for videos with platform-provided subtitles, not download-only work or audio-only ASR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download and run BBDown or yt-dlp and modify the user's persistent PATH. <br>
Mitigation: Install only when the user is comfortable with those changes, prefer official downloads, verify binaries where possible, and avoid persistent PATH changes unless desired. <br>
Risk: Restricted videos may require browser or session cookies. <br>
Mitigation: Use cookies only after explicit approval, never paste cookie contents into chat, prefer file paths over raw cookie values, and delete one-off cookie files after use. <br>
Risk: Cleanup commands could remove files if pointed at the wrong folder. <br>
Mitigation: Run cleanup only inside a newly created per-video output directory and keep final transcript files separate from intermediate artifacts. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/hqwqf/videolink-to-article) <br>
- [Authentication & Cookies Guide](references/auth.md) <br>
- [Subtitle Cleanup Guide](references/cleanup_guide.md) <br>
- [Tool Installation Guide](references/install_tools.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Worked Example](references/worked_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown transcript files with supporting command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-language transcript deliverables and may create temporary subtitle, metadata, and normalization files during processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
