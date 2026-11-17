## Description:

Turn user-requested text, assistant answers, briefings or messages into an audio file with PyAI Speak text-to-speech using the official CLI. Discover available voices and return playable output. Requires a PyAI account and speech permissions; does not place calls, clone voices or send messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomsai](https://clawhub.ai/user/atomsai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn text they explicitly request into speech and receive a playable audio file. The skill also helps users select an available voice and verify the PyAI project and speech permission before synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis sends submitted text to the selected PyAI project and consumes project usage.

Mitigation: Confirm the intended project and speech permission, and submit only text the user is comfortable sending to PyAI.

## Reference(s):

- [PyAI Speak overview](https://pyai.com/mcp)
- [PyAI Speak on ClawHub](https://clawhub.ai/atomsai/skills/pyai-speak)

## Skill Output:

**Output Type(s):** [Audio file, Shell commands]

**Output Format:** [Playable WAV audio by default; MP3 when requested and supported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech reflects the requested text; each request is limited to 2,000 characters.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
