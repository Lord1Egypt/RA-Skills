## Description:

Generates standalone speech audio from text using HeyGen's Starfish TTS model, including voice listing, voice selection, speed control, SSML pauses, and multilingual locale options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelwang11394](https://clawhub.ai/user/michaelwang11394)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to list HeyGen Starfish-compatible voices and generate standalone speech audio for voiceovers, narration, podcasts, and related text-to-speech workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent needs access to a HeyGen API key.

Mitigation: Provide HEYGEN_API_KEY only in environments where the agent is approved to call HeyGen, and avoid exposing the key in prompts, logs, or generated examples.

Risk: Text chosen for speech generation is sent to HeyGen.

Mitigation: Do not submit confidential, regulated, or sensitive text unless that external processing is approved for the use case.

Risk: Broad HeyGen MCP tools may expose actions beyond the named text-to-speech workflow.

Mitigation: Prefer the named TTS tools when available and review any broader HeyGen MCP action before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelwang11394/skills/text-to-speech-heygen)
- [HeyGen Starfish voice listing endpoint](https://api.heygen.com/v3/voices?engine=starfish)
- [HeyGen speech generation endpoint](https://api.heygen.com/v3/voices/speech)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with curl, TypeScript, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HEYGEN_API_KEY and returns HeyGen voice metadata or generated audio URLs when the agent performs the described API calls.]

## Skill Version(s):

2.23.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
