## Description:

QCut Toolkit routes media workflow requests across project setup, FFmpeg processing, AI content generation and analysis, QCut editor control, video prompt writing, MCP preview testing, and PR review processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donghaozhang](https://clawhub.ai/user/donghaozhang)

### License/Terms of Use:


## Use Case:

Developers, media creators, and QCut users use this skill to organize media projects, transform video and audio, generate or analyze AI media, prepare subtitles, and guide editor automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit may start local review servers for media and subtitle workflows.

Mitigation: Run the servers only in a controlled local environment and avoid exposing them to other devices or webpages.

Risk: Some workflows upload audio or video to public hosting and cloud AI providers.

Mitigation: Do not use confidential media unless those external transfers are acceptable for the project.

Risk: Credential handling includes plaintext or local skill-directory patterns.

Mitigation: Keep secrets out of .claude/skills and prefer controlled credential stores or environment handling.

Risk: The bundled self-evolve sub-skill can update skill guidance based on feedback.

Mitigation: Avoid or disable the self-evolve sub-skill unless changes are reviewed before use.

## Reference(s):

- [QCut Toolkit ClawHub Release](https://clawhub.ai/donghaozhang/skills/qcut-toolkit)
- [AI Content Pipeline Reference](ai-content-pipeline/REFERENCE.md)
- [AI Content Pipeline Examples](ai-content-pipeline/EXAMPLES.md)
- [FFmpeg Concepts](ffmpeg-skill/CONCEPTS.md)
- [FFmpeg Command Reference](ffmpeg-skill/REFERENCE.md)
- [FFmpeg Advanced Workflows](ffmpeg-skill/ADVANCED.md)
- [Volcengine Speech Recognition Console](https://console.volcengine.com/speech/new/experience/asr?projectName=default)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration examples, and generated media workflow files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create QCut project folders, media outputs, subtitle JSON/SRT files, review HTML, and editor/API commands depending on the selected sub-skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
