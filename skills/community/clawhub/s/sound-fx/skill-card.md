## Description: <br>
Generate short sound effects via ElevenLabs SFX (text-to-sound). Use when you need SFX clips like applause, canned laughter, whooshes, ambience, or short stingers, and optionally convert to WhatsApp-friendly .ogg/opus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javicasper](https://clawhub.ai/user/javicasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate short audio effects from text prompts and save the resulting media file for use in messages, demos, or media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sound-effect prompts are sent to ElevenLabs and may include sensitive or confidential details if supplied by the user. <br>
Mitigation: Avoid putting secrets, private data, or confidential project details in prompts. <br>
Risk: Requests use the configured ElevenLabs API key and may affect quota or billing. <br>
Mitigation: Use an appropriate API key, review provider account limits, and monitor usage. <br>
Risk: The script writes the returned audio directly to the output path provided by the user. <br>
Mitigation: Choose output paths carefully and avoid overwriting important files. <br>


## Reference(s): <br>
- [Sound FX on ClawHub](https://clawhub.ai/javicasper/sound-fx) <br>
- [ElevenLabs sound generation API endpoint](https://api.elevenlabs.io/v1/sound-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an MP3 file by default and prints the saved media path on success.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
