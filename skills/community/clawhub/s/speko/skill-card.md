## Description:

Speko helps agents transcribe audio, synthesize speech, and route STT, LLM, and TTS requests across benchmarked models with language, cost, and failover controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speko](https://clawhub.ai/user/speko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preview Speko speech-model routes, transcribe recordings, synthesize WAV audio, and run OpenAI-shaped LLM turns through Speko with one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text, audio recordings, and routed LLM prompts may be sent to Speko using SPEKO_API_KEY.

Mitigation: Use only with data permitted by Speko's terms and avoid confidential recordings, third-party conversations, or sensitive prompts unless approved.

Risk: Misconfigured keys, unsupported languages, or incorrect routing constraints can produce failed or misleading routing results.

Mitigation: Preview routes before spending, use the routing preview as the authority for enabled languages, and read route response headers instead of assuming a pinned model won.

Risk: Speech synthesis or transcription responses can appear successful while yielding unusable or empty media in documented edge cases.

Mitigation: Use buffered WAV speech output, let curl set multipart boundaries, convert audio to WAV where needed, and assert on output bytes or transcript content.

## Reference(s):

- [Speko ClawHub skill](https://clawhub.ai/speko/skills/speko)
- [Speko API base](https://api.speko.ai/v1)
- [Speko routing preview endpoint](https://api.speko.ai/v1/routing/preview?stage=tts&language=en&objective=quality)
- [Speko speech synthesis endpoint](https://api.speko.ai/v1/audio/speech)
- [Speko audio transcription endpoint](https://api.speko.ai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, API request examples, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Speko API requests that send selected text, audio, or routed LLM prompts using SPEKO_API_KEY; speech synthesis examples write WAV audio.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
