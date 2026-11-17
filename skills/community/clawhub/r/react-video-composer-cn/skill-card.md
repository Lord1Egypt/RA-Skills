## Description:

基于Remotion的React视频制作工具，提供文字转视频、字幕同步、动画编排、数据可视化、品牌片头制作、分镜表规划与转场效果，适用于产品演示、社交短视频和教育培训课件等视频内容生产场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content producers use this skill to turn video briefs, scripts, audio, or datasets into Remotion-based React video projects with scene structure, subtitles, animation, render commands, and optional voiceover or transcription workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local Remotion or npm commands and write generated project files.

Mitigation: Run it in a sandboxed workspace, review commands before execution, and inspect generated files before rendering or publishing.

Risk: Callback URLs and third-party service credentials may expose sensitive data if used carelessly.

Mitigation: Use callback URLs only when needed, confirm the exact endpoint and data sent, and keep all credentials in environment variables instead of project files or logs.

Risk: The security scan flags under-scoped API, callback, file, and command-execution behavior.

Mitigation: Review the skill behavior before installation and limit agent permissions to the files, commands, and network endpoints required for the intended video project.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with React/TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project files under output/{project-name}/src/, script.md storyboards, Remotion render commands, and setup guidance for Node.js, Remotion, Chrome/Chromium, FFmpeg, TTS, and transcription tooling.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
