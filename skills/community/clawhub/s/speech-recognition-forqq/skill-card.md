## Description: <br>
Converts QQ voice messages and AMR/SILK audio files to text using pysilk decoding and faster-whisper transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yvanboyang](https://clawhub.ai/user/yvanboyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe QQ voice messages and AMR/SILK audio into text as part of speech recognition workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes dependency installation, model download, local file access, and audio transcription steps. <br>
Mitigation: Review the visible skill page and files before enabling it, confirm that install commands and model sources match expectations, and run it only with audio files intended for transcription. <br>
Risk: The security evidence reports a clean verdict but notes that a full artifact coherence check was not available to the scanner. <br>
Mitigation: Validate the artifact contents against the release page and expected behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yvanboyang/speech-recognition-forqq) <br>
- [Publisher profile](https://clawhub.ai/user/yvanboyang) <br>
- [Systran faster-whisper-base model](https://huggingface.co/Systran/faster-whisper-base) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks; runtime transcription returns text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local audio files, Python dependencies, and a faster-whisper model directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
