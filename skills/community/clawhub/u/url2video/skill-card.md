## Description:

Converts a website URL into a promotional video workflow using Remotion, React, content extraction, narration, subtitles, background music, and review screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn a public website URL into a short promotional video project with brand colors, animated scenes, Chinese narration, subtitles, background music, still previews, and an MP4 render path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches websites and downloads packages or media during setup.

Mitigation: Run it only in a restricted workspace with minimal credentials and network access, and use public, non-sensitive website URLs.

Risk: Generated project files and dependency installs may introduce unreviewed code or packages.

Mitigation: Review generated files before installing or building, and prefer pinned dependencies, a lockfile, and local Remotion binaries over npx-fetched commands.

Risk: The scaffold script accepts brand names for filesystem and code paths with weak input scoping.

Mitigation: Validate brand names as simple slugs before running the scaffold script.

## Reference(s):

- [Component template](references/component-template.tsx)
- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/url2video)
- [Pixabay background music asset](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=electronic-future-beats-117998.mp3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, TypeScript, and configuration snippets; generated project files and media output paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Remotion project, narration script, review stills, and MP4 output path; rendering depends on website accessibility, local tools, and available system resources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
