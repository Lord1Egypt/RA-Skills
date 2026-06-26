## Description: <br>
Video Notes turns YouTube and Bilibili videos into structured single-file HTML notes with summaries, subtitle search, SVG diagrams, and optional keyframe screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaimomo99](https://clawhub.ai/user/kaimomo99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and knowledge workers use this skill to convert YouTube or Bilibili videos into searchable study notes, summaries, diagrams, transcripts, and keyframe galleries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use browser login cookies to access video subtitles. <br>
Mitigation: Avoid browser-cookie access unless needed; prefer a narrowly scoped cookies file and delete /tmp/yt-cookies-export.txt after use. <br>
Risk: The skill can modify the Python environment while running. <br>
Mitigation: Run it in an isolated environment with a preinstalled, pinned yt-dlp dependency. <br>
Risk: Generated local HTML notes can contain video-derived content and transcripts. <br>
Mitigation: Treat generated note artifacts as content-bearing files and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaimomo99/video-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Single-file HTML notes document with JSON subtitle and keyframe data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language follows the user's request language; keyframe screenshots require ffmpeg and may be omitted when unavailable.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, skill.json, changelog released 2026-05-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
