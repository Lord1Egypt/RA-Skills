## Description: <br>
Generate a narrated Remotion video from an Excalidraw (.excalidraw) diagram using text-to-speech (macOS say) and render to MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack4world](https://clawhub.ai/user/jack4world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to turn Excalidraw diagrams and voiceover scripts into narrated MP4 explainer videos with pan, zoom, focus highlights, subtitles, and configurable TTS backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud TTS modes can expose API keys and voiceover text in command logs or to external providers. <br>
Mitigation: Use the default local say backend or provide an existing voiceover MP3 for sensitive content; avoid cloud TTS in shared logs or CI unless credentials and payloads are redacted. <br>
Risk: Rendering installs npm dependencies in the temporary Remotion project. <br>
Mitigation: Review dependencies and run the skill in a trusted environment before using it with sensitive diagrams or scripts. <br>


## Reference(s): <br>
- [Storyboard schema](references/storyboard.schema.json) <br>
- [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals) <br>
- [Remotion configuration](https://remotion.dev/docs/config) <br>
- [OpenAI audio speech API](https://platform.openai.com/docs/api-reference/audio/createSpeech) <br>
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON storyboard configuration, and generated MP4 file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate local voiceover audio, copy a Remotion template project, install npm dependencies, and render a video file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
