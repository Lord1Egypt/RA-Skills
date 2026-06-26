## Description: <br>
MiniMax Music Generation helps agents create lyrics, generate music from lyrics or style prompts, and save generated lyrics and audio files through MiniMax music APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbos7](https://clawhub.ai/user/turbos7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to route song ideas, lyrics, style prompts, and optional reference-audio inputs through MiniMax for lyric drafting, full song creation, instrumental generation, and cover-style music generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, titles, and reference-audio URLs may be sent to MiniMax using the user's API key. <br>
Mitigation: Do not submit secrets, regulated data, or proprietary lyrics unless MiniMax account terms and data-handling requirements allow it. <br>
Risk: The skill can consume MiniMax API quota or paid usage. <br>
Mitigation: Monitor API usage and costs for the MINIMAX_API_KEY used by the agent. <br>
Risk: Generated lyrics and audio are saved locally and may persist after the task is complete. <br>
Mitigation: Store outputs only in appropriate workspaces and delete generated lyric or audio files when no longer needed. <br>


## Reference(s): <br>
- [MiniMax Lyrics Generation API Reference](references/lyrics-api.md) <br>
- [MiniMax Music Generation API Reference](references/music-api.md) <br>
- [MiniMax API key page](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [ClawHub release page](https://clawhub.ai/turbos7/turbos7-minimax-music) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples, generated lyric text files, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MINIMAX_API_KEY and can save lyrics under ~/.openclaw/workspace/assets/music/lyrics and audio under ~/.openclaw/workspace/assets/music.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
