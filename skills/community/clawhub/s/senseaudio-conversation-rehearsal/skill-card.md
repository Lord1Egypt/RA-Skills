## Description:

Conversation Rehearsal helps agents run voice-first practice for high-pressure workplace conversations using AudioClaw ASR/TTS, counterpart simulation, and transcript debriefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, coaches, and HR or manager-training teams use this skill to rehearse high-pressure conversations such as performance reviews, promotion defenses, reporting meetings, difficult manager conversations, and stakeholder alignment sessions. The agent helps define the scenario, simulate counterpart pressure, transcribe spoken replies, and produce a concrete debrief with rewrite guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access SenseAudio credentials and may fall back to a logged-in Chrome session.

Mitigation: Prefer explicit API keys and prepared clone voice IDs, and disable Chrome/browser-session fallback unless explicitly approved.

Risk: The skill can create or manage authorized voice clones.

Mitigation: Use proxy voice by default and use cloned voices only with explicit consent and a prepared voice ID.

Risk: Rehearsal transcripts and generated audio may contain sensitive workplace content.

Mitigation: Treat generated files as sensitive and store, share, or delete them according to the user's data-handling policy.

Risk: Generated counterpart audio can be sent to Feishu.

Mitigation: Keep Feishu sending disabled unless the destination chat is confirmed.

## Reference(s):

- [Live Rehearsal Loop](artifact/references/live_rehearsal_loop.md)
- [Rehearsal Design](artifact/references/rehearsal_design.md)
- [ClawHub Skill Page](https://clawhub.ai/kikidouloveme79/skills/senseaudio-conversation-rehearsal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio]

**Output Format:** [Markdown guidance with inline shell commands, JSON artifacts, transcript analysis, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AudioClaw ASR/TTS services, write local rehearsal artifacts, and optionally send counterpart audio to Feishu when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
