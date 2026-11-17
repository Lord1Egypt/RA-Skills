## Description:

Videogen automates WeChat Channels short-video production by turning a topic or supported article URL into a script, storyboard, narration, AI-generated clips, Remotion visuals, FFmpeg edits, and publish-ready video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devioslang](https://clawhub.ai/user/devioslang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video-production operators use this skill to generate short-form vertical videos from topics or supported source articles, including storyboards, narration, visual project files, AI video clips, and final mixed video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that implementation flaws could expose API keys or sensitive fetched content.

Mitigation: Use isolated workspaces with limited filesystem and network access, and use throwaway or tightly scoped API keys.

Risk: The security review reports that untrusted URLs or narration can increase exposure when content is fetched, summarized, or transformed.

Mitigation: Avoid feeding untrusted URLs or narration into the pipeline; avoid --summarize with MiniMax keys until provider routing is fixed.

Risk: The security review reports that generated code or commands may be executed from user-provided text.

Mitigation: Review generated scripts, commands, and project files before execution, especially before installing dependencies or rendering assets.

Risk: The security review advises against forceful operations on paths that may contain important files.

Mitigation: Do not run --force on any path unless its contents are disposable or already backed up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devioslang/skills/videogen)
- [Apple Remotion template README](templates/apple/README.md)
- [Evaluation prompts](evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, JSON storyboards, generated Remotion project files, shell commands, audio/video files, and final MP4 assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce intermediate assets such as scripts, voiceover audio, slide imagery, AI-generated clips, concat lists, Remotion projects, and FFmpeg-rendered video outputs.]

## Skill Version(s):

2.2.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
