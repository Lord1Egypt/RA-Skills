## Description:

Analyzes Douyin, Bilibili, and Xiaohongshu video links by downloading video, transcribing speech locally with faster-whisper, and producing structured analysis plus an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can turn a single supported short-video link into transcripts, structured content analysis, quotable highlights, and a browser-viewable HTML report. It is suited for content review, summarization, and creator-oriented analysis when the user has rights to process the source video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unescaped analysis or transcript-derived content that may execute browser code when opened.

Mitigation: Treat generated HTML as untrusted, review or sanitize fields before opening or sharing reports, and prefer escaping all analysis fields in the renderer.

Risk: The workflow downloads media from third-party video platforms and may process private, sensitive, or copyrighted content.

Mitigation: Process only user-intended links, avoid sensitive videos, confirm rights before downloading or transcribing content, and do not expose the tool to unverified URLs.

Risk: Cookie files may be used for platform authentication.

Mitigation: Pass cookies only when required, keep cookie files local, and run the skill in an isolated environment with controlled file access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/tri-platform-video-analysis)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON schemas, transcript text files, analysis JSON, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one supported video link at a time; generated outputs are written under the configured output directory.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
