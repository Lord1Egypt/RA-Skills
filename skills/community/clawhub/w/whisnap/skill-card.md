## Description: <br>
macOS CLI for transcribing audio and video files using local Whisper models or Whisnap Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neolio42](https://clawhub.ai/user/Neolio42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run Whisnap CLI transcription workflows for local audio and video files, including optional JSON timestamp output and optional Whisnap Cloud transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud transcription may send recordings to Whisnap Cloud. <br>
Mitigation: Use local transcription for private recordings unless cloud processing is intentionally selected. <br>
Risk: The skill depends on a local whisnap binary installed outside the skill. <br>
Mitigation: Install Whisnap only from a trusted source and verify the CLI is the expected Whisnap binary before use. <br>


## Reference(s): <br>
- [Whisnap homepage](https://whisnap.com) <br>
- [ClawHub skill page](https://clawhub.ai/Neolio42/whisnap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands produce transcript text or structured JSON with segments, timestamps, model information, and processing time when the Whisnap CLI is installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
