## Description:

Use when a game, interactive story, or virtual world needs reusable NPC voice behavior, including fixed voice identity, catchphrases, relationship-aware dialogue, player voice intake through AudioClaw ASR, task briefings, narration, and event announcements synthesized with AudioClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and narrative designers use this skill to create consistent NPC voice behavior for games and interactive worlds, including relation-aware dialogue, event announcements, and ASR-driven replies to player input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player audio, dialogue text, synthesized NPC audio, and Feishu message metadata may be sent to external services.

Mitigation: Use dedicated least-privilege API credentials, confirm the destination service and chat before sending, and avoid processing sensitive player content unless the user has approved the workflow.

Risk: Generated audio can be automatically sent to Feishu when sticky voice mode or send flags are used.

Mitigation: Keep auto-send mode scoped to an explicit session and chat, review generated lines before delivery when practical, and switch to text-only output when voice delivery is not intended.

Risk: The skill uses local credential and helper discovery and writes transcripts, manifests, and audio artifacts to disk.

Mitigation: Run it in a controlled workspace, review the helper modules it loads, restrict file permissions for generated artifacts, and delete retained voice or transcript files when no longer needed.

## Reference(s):

- [NPC Voice Design](references/npc_voice_design.md)
- [AudioClaw ASR player loop](references/asr_player_loop.md)
- [ClawHub skill page](https://clawhub.ai/kikidouloveme79/skills/senseaudio-game-npc-director)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, API Calls]

**Output Format:** [Markdown guidance with shell commands, JSON manifests, transcript files, synthesized audio files, and optional Feishu delivery records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external AudioClaw ASR/TTS services and optionally Feishu; outputs can include player transcripts, NPC scene manifests, MP3 audio, OGG/Opus audio, and JSON result summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
