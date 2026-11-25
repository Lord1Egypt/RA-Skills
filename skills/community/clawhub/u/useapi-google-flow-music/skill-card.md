## Description:

Make full AI songs with vocals or instrumentals on Google's Lyria 3.5 and Lyria 3 Pro in Google Flow Music on your own Google Flow Music plan (Free, or the one included with Google AI Plus, Pro or Ultra), through the useapi.net Google Flow Music API, a third-party paid API not affiliated with Google. Song from a text prompt, your own lyrics or lyrics the model writes, AI lyrics writing, and stems (drums, bass, vocals, other). Saves .m4a, .wav or .mp3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useapi](https://clawhub.ai/user/useapi)

### License/Terms of Use:

MIT-0

## Use Case:

People creating music with Google Flow Music can use the skill to turn prompts or supplied lyrics into songs, draft lyrics, download audio, and split completed tracks into stems. It requires a useapi.net account and token plus a connected Google Flow Music account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a benign verdict with medium confidence and incomplete coverage; some references were unresolved.

Mitigation: Review the skill and unresolved references before installation, and use it only if you trust the useapi.net service.

Risk: The skill requires a useapi.net API token and uses the connected Google Flow Music account, which may consume its credits.

Mitigation: Keep the token private, configure it only in the intended environment, and check account credit costs before generating songs or stems.

## Reference(s):

- [useapi.net Google Flow Music API documentation](https://useapi.net/docs/api-flowmusic-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow-music)
- [Connect a Google Flow Music account](https://useapi.net/docs/start-here/setup-flowmusic)
- [useapi.net account and API token setup](https://useapi.net/docs/start-here/setup-useapi)
- [useapi.net subscription](https://useapi.net/docs/subscription)
- [ClawHub skill page](https://clawhub.ai/useapi/skills/useapi-google-flow-music)

## Skill Output:

**Output Type(s):** [Audio files, Lyrics, Text, JSON, Shell commands]

**Output Format:** [M4A, WAV, or MP3 audio files; plain-text lyrics; JSON job records; command-line progress and saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A song request may produce one or two clips; stem splitting produces drums, bass, vocals, and other audio files.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
