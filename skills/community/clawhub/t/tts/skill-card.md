## Description: <br>
Converts text to MP3 speech audio using the Hume AI API or a legacy OpenAI text-to-speech script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AMSTKO](https://clawhub.ai/user/AMSTKO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to turn provided text into a voice reply or audio message, producing a local MP3 file that can be sent back to the requester. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to an external provider API. <br>
Mitigation: Send only text appropriate for the selected provider and use the API key for the provider being invoked. <br>
Risk: A caller-provided output path could overwrite an existing local file. <br>
Mitigation: Choose a dedicated output filename or directory for generated MP3 files. <br>
Risk: Providing unnecessary credentials can expand exposure if the runtime environment is shared. <br>
Mitigation: Set only the API key required for the selected provider; do not set unused secrets unless the publisher clarifies a need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AMSTKO/tts) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP3 audio file plus command output with an absolute MEDIA path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a provider API key for Hume AI or OpenAI and writes to a caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
