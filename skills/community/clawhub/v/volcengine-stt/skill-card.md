## Description:

Transcribe audio to text using Volcano Engine (Volcengine/ARK) speech-to-text APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe local audio files with Volcengine speech-to-text services, including OpenClaw voice-message workflows that need a replacement for Whisper/OpenAI STT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script may upload audio to hardcoded ByteDance AUC endpoints using VOLC credentials, while the user-facing documentation describes ARK configuration.

Mitigation: Review the destination endpoints, credential source, and billable usage model before installing or running the skill.

Risk: Credentials can be read from machine-local OpenClaw configuration as a fallback.

Mitigation: Confirm the local OpenClaw configuration only contains intended VOLC credentials for this skill and avoid committing secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/volcengine-stt)
- [Publisher profile](https://clawhub.ai/user/reed1898)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Plain text transcript file by default, or raw JSON response when requested; the script prints the output file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine credentials and uploads audio to external speech-to-text API endpoints.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
