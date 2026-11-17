## Description:

MiniMax TTS helps agents use MiniMax APIs to convert text into speech, manage voices, and create cloned voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to synthesize spoken audio from text, select or manage MiniMax voices, and create cloned voices through MiniMax APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text, task metadata, voice IDs, voice-cloning inputs, and API credentials may be sent to MiniMax.

Mitigation: Use MINIMAX_API_KEY, avoid sensitive text and unauthorized voice samples, and run the skill only with data approved for MiniMax processing.

Risk: Voice cloning and deletion can affect account voices, including deletion of custom voices documented as unrecoverable.

Mitigation: Confirm consent and rights for voice samples, and manually verify voice IDs before cloning or deletion.

Risk: The server security verdict is suspicious because the skill sends data to a third-party service and has limited safeguards around voice management.

Mitigation: Review the commands before execution, prefer environment-based credentials over command-line API keys, and limit use to trusted MiniMax accounts.

## Reference(s):

- [Async TTS API Reference](references/tts-async.md)
- [Sync TTS API Reference](references/tts-sync.md)
- [Voice Clone API Reference](references/voice-clone.md)
- [Voice Management API Reference](references/voice-management.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When synthesis scripts are executed, they can save generated audio files under ~/.openclaw/workspace/assets/audios.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
