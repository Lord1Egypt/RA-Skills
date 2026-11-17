## Description:

Transform YouTube videos into podcast-style voice summaries using ElevenLabs TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franciscoandsam](https://clawhub.ai/user/franciscoandsam)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn YouTube URLs into short spoken summaries, text summaries, teaser text, and key takeaways through a configured backend service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external backend with API keys.

Mitigation: Review the backend before installation, pin it to a known commit, prefer npm ci with a lockfile, and run it in a restricted environment.

Risk: YouTube URLs, transcripts, summaries, and generated audio may be handled by ElevenLabs, Supadata, OpenRouter, and the configured backend.

Mitigation: Avoid submitting private or sensitive YouTube links unless that third-party processing is acceptable.

Risk: API keys for ElevenLabs, Supadata, and OpenRouter can create spend or data-access exposure if leaked or over-scoped.

Mitigation: Use narrowly scoped, revocable keys with spending limits and rotate them if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franciscoandsam/skills/youtube-voice-summarizer-elevenlabs)
- [Publisher profile](https://clawhub.ai/user/franciscoandsam)
- [ElevenLabs](https://elevenlabs.io)
- [Supadata](https://supadata.ai)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an MP3 audio URL, teaser text, full summary, and key points when the backend job completes; can also produce text-only summaries.]

## Skill Version(s):

1.0.0 (source: evidence.release, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
