## Description:

Text-to-Speech and Speech-to-Text integration using Resemble AI HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adriano-vr](https://clawhub.ai/user/adriano-vr)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate MP3 speech from text and transcribe audio files through Resemble AI API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text and transcription audio are sent to Resemble AI using the user's API key.

Mitigation: Avoid confidential, regulated, or highly personal content unless Resemble AI's terms and data handling meet the user's requirements.

Risk: The TTS script writes generated audio to a temporary MP3 path.

Mitigation: Review and harden temporary-file handling before deploying in shared or sensitive environments.

Risk: The TTS script constructs a JSON request payload from command-line text.

Mitigation: Validate or escape input when adapting the script for automated or untrusted text sources.

## Reference(s):

- [Resemble AI Speech-to-Text API endpoint](https://app.resemble.ai/api/v2/speech-to-text)
- [Resemble AI synthesis API endpoint](https://f.cluster.resemble.ai/synthesize)
- [ClawHub skill page](https://clawhub.ai/adriano-vr/skills/ressemble)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text transcripts, MEDIA file paths for generated MP3 audio, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RESEMBLE_API_KEY and sends synthesis text or transcription audio to Resemble AI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
