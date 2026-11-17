## Description:

Generate a narrated Remotion video from an Excalidraw (.excalidraw) diagram using text-to-speech (macOS say) and render to MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack4world](https://clawhub.ai/user/jack4world)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to convert Excalidraw diagrams and voiceover scripts into narrated MP4 explainer videos with camera movement, focus highlights, subtitles, and optional storyboard control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud TTS backends can send narration text to OpenAI or ElevenLabs.

Mitigation: Use local macOS say or a prebuilt MP3 for sensitive narration unless cloud TTS sharing is acceptable.

Risk: API keys may be exposed in command logs when cloud TTS is used.

Mitigation: Avoid cloud TTS until command logging is corrected, or use tightly scoped temporary keys and review logs.

Risk: The optional workdir flow deletes an existing remotion-excalidraw-tts subdirectory.

Mitigation: Use an empty disposable workdir and do not run the script with elevated privileges.

Risk: Runtime npm installs may fetch dependencies during execution.

Mitigation: Review the package lock and run in a controlled environment before using the rendered output workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jack4world/skills/remotion-excalidraw-tts)
- [storyboard.schema.json](artifact/references/storyboard.schema.json)
- [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [Remotion config documentation](https://remotion.dev/docs/config)
- [OpenAI speech API reference](https://platform.openai.com/docs/api-reference/audio/createSpeech)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON storyboard configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local project files and renders an MP4 through Remotion when the generated command is run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
