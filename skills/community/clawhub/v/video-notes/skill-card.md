## Description:

Video Notes turns YouTube and Bilibili videos into self-contained HTML notes with extracted subtitles, structured summaries, keyframes, SVG diagrams, sidebar navigation, and transcript search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaimomo99](https://clawhub.ai/user/kaimomo99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, researchers, and knowledge workers use this skill to convert public or authenticated YouTube and Bilibili videos into searchable study notes, summaries, diagrams, and timestamped keyframe galleries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-cookie mode can expose active browser sessions or leave exported cookies in temporary files.

Mitigation: Avoid using private, paid, or sensitive accounts; run in an isolated environment; and delete /tmp/yt-cookies-export.txt after any cookie-based run.

Risk: The subtitle and keyframe scripts may install or run video-download tooling locally.

Mitigation: Review the scripts before use and run them with pinned dependencies in an isolated Python environment.

Risk: Generated HTML may include content derived from untrusted captions.

Mitigation: Treat generated HTML as active content, inspect it before sharing, and open it in a constrained local environment when processing untrusted videos.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaimomo99/skills/video-notes)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kaimomo99)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated single-file HTML output; subtitle and keyframe intermediates are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keyframe capture requires ffmpeg; browser-cookie mode may create temporary cookie files under /tmp.]

## Skill Version(s):

1.1.0 (source: frontmatter, skill.json, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
