## Description:

Smart TTS synthesizes speech by automatically trying supported DashScope models and voices until generation succeeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate single or batch WAV speech files from text with fallback across available DashScope model and voice combinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to DashScope.

Mitigation: Do not submit secrets, private records, or confidential business content.

Risk: Generated WAV files may overwrite existing files at the configured output path.

Mitigation: Check or change the output path before running single or batch generation.

Risk: The skill requires a DashScope API key.

Mitigation: Provide DASHSCOPE_API_KEY through the environment and avoid placing credentials in shared files.

## Reference(s):

- [ClawHub smart-tts skill page](https://clawhub.ai/ppop0uuiu/skills/smart-tts)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions]

**Output Format:** [WAV audio files with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DASHSCOPE_API_KEY and writes generated audio to the OpenClaw workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
