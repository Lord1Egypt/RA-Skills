## Description:

Tts Voice Ai helps agents generate multilingual speech audio with MiniMax, including Chinese, English, Japanese, Korean, Cantonese, dubbing, audiobook-style narration, and voice-clone voice IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiachuan-1](https://clawhub.ai/user/jiachuan-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to convert text into speech files for multilingual voice generation, dubbing, narration, voice announcements, and customer-service audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to MiniMax.

Mitigation: Do not synthesize secrets, regulated data, or confidential material unless that use has been approved.

Risk: Voice cloning can create consent and misuse concerns.

Mitigation: Use cloned voices only when the voice owner has clearly permitted that use.

Risk: The runtime depends on the Python requests package.

Mitigation: Pin and review the requests dependency in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiachuan-1/skills/tts-voice-ai)
- [MiniMax platform](https://platform.minimax.io)
- [MiniMax China API endpoint](https://api.minimaxi.com)
- [MiniMax international API endpoint](https://api.minimax.io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output is local audio files such as MP3, WAV, or FLAC.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and MINIMAX_API_KEY; generated text is sent to MiniMax and audio is written locally.]

## Skill Version(s):

1.1.0 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
