## Description: <br>
Converts Chinese or English text, including text extracted from images, into natural-sounding MP3 speech with selectable Edge TTS voices and speech rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[figo6228-spec](https://clawhub.ai/user/figo6228-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn lessons, stories, essays, articles, or OCR text into MP3 narration. It supports single-file and batch conversion with Chinese and English voice choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text, including OCR text from images, is sent to Microsoft's online TTS service. <br>
Mitigation: Use only when the user is comfortable sending the text to that service, and avoid submitting sensitive or confidential content. <br>
Risk: The setup helper may install the edge-tts package into the active Python environment. <br>
Mitigation: Run setup in a virtual environment where possible and review dependency installation before use. <br>
Risk: Mismatching text language and voice language can produce accented or lower-quality narration. <br>
Mitigation: Detect the text language first and choose a matching Chinese or English voice before generating audio. <br>


## Reference(s): <br>
- [Voice Catalog](references/voice_catalog.md) <br>
- [ClawHub skill page](https://clawhub.ai/figo6228-spec/text-to-audio) <br>
- [Publisher profile](https://clawhub.ai/user/figo6228-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON batch configuration, and generated MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is MP3; batch mode reads a JSON configuration file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
