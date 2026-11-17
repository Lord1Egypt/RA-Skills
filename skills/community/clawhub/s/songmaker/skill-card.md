## Description:

Generate a complete song from a text description by drafting lyrics, composing music, and returning downloadable audio and cover art links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create songs, background music, or audio from a description or supplied lyrics through SenseAudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell examples insert user-supplied prompts, lyrics, titles, and style text directly into command payloads.

Mitigation: Rewrite command examples to construct JSON with jq or another serializer before using untrusted user text.

Risk: Prompts and lyrics may contain sensitive or private material sent to an external song-generation service.

Mitigation: Use the skill only with non-sensitive prompts and lyrics unless the user has reviewed and accepted the service handling requirements.

Risk: Literal use of the snippets with untrusted inputs could expose API keys or local files through shell injection.

Mitigation: Treat snippets as examples, quote variables safely, avoid shell evaluation of user text, and keep SENSEAUDIO_API_KEY out of logs and shared output.

## Reference(s):

- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)
- [ClawHub Songmaker skill page](https://clawhub.ai/scikkk/skills/songmaker)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance, Text]

**Output Format:** [Markdown with bash command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; returns song status, title, duration, audio URL, and cover art URL on success.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
