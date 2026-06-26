## Description: <br>
Transcribe audio to text with Whisper models through the inference.sh CLI, including translation, multilingual transcription, and optional timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and teams use this skill to run inference.sh Whisper transcription workflows for meetings, podcasts, subtitles, voice notes, interviews, and accessibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs the inference.sh CLI, so users may execute provider-supplied tooling and generated shell commands. <br>
Mitigation: Install the CLI only from trusted inference.sh sources, prefer the documented manual checksum verification path, and review `infsh` commands before running them. <br>
Risk: Audio and video inputs may contain confidential, regulated, or private information and are processed through inference.sh workflows. <br>
Mitigation: Use only recordings approved for inference.sh processing under the user's account and avoid submitting sensitive data unless organizational approval is in place. <br>


## Reference(s): <br>
- [Speech To Text on ClawHub](https://clawhub.ai/okaris/speech-to-text) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Audio Transcription Example](https://inference.sh/docs/examples/audio-transcription) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [Manual CLI Checksum Verification](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced inference.sh apps return JSON containing transcription text, detected language, and timestamped segments when requested.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
