## Description:

Generates lyrics and music with MiniMax APIs, supporting full-song creation, lyric editing or continuation, instrumental tracks, and cover-style generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate song lyrics, create music from lyrics or style prompts, save generated lyric and audio files, and run helper scripts for one-step song creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Song prompts, lyrics, and related metadata are sent to MiniMax APIs.

Mitigation: Use the skill only for content that is acceptable to share with MiniMax under the user's applicable data handling requirements.

Risk: The helper accepts an API key through command-line arguments as well as the MINIMAX_API_KEY environment variable.

Mitigation: Prefer MINIMAX_API_KEY from an environment variable or secret manager instead of passing credentials on the command line.

Risk: Downloaded audio is written locally from the returned URL without constraining URL origin or file size.

Mitigation: Review generated audio files after download and use the skill in an environment where large or unexpected downloads are acceptable.

## Reference(s):

- [MiniMax Lyrics Generation API Reference](references/lyrics-api.md)
- [MiniMax Music Generation API Reference](references/music-api.md)
- [MiniMax Interface Key Settings](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [ClawHub Skill Page](https://clawhub.ai/turbos7/skills/turbos7-minimax-music)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python and shell examples; generated lyrics as text files and generated music as audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and may save files under ~/.openclaw/workspace/assets/music.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
