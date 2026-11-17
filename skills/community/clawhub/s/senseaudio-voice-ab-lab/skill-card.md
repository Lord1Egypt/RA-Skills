## Description:

Use when a team wants to generate multiple ad, spoken-copy, sales, or promo voice variants from one typed or spoken creative brief, transcribe voice memos with AudioClaw ASR, and synthesize the variants with the same AudioClaw voice_id for A/B testing, regional wording experiments, or rapid commercial validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Commercial marketing, sales, and content teams use this skill to turn typed campaign briefs or spoken voice memos into multiple same-voice copy and audio variants for A/B review, regional wording tests, and rapid validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefs, transcripts, generated copy, and synthesized audio may be sent to SenseAudio and optionally to Feishu.

Mitigation: Use dedicated API and Feishu credentials, provide explicit chat IDs, review result JSON before Feishu delivery, and avoid processing unrelated private audio in the same workspace.

Risk: The security summary reports unsafe helper loading and broad credential use.

Mitigation: Review helper-loading paths and credential scope before installation; run in a constrained workspace until path validation and helper-loading issues are fixed.

## Reference(s):

- [Commercial Voice A/B Patterns](references/commercial_ab_patterns.md)
- [AudioClaw ASR brief intake](references/asr_brief_pipeline.md)
- [AudioClaw ASR API endpoint](https://api.senseaudio.cn/v1/audio/transcriptions)
- [AudioClaw platform API](https://platform.senseaudio.cn/api)
- [AudioClaw TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2)
- [ClawHub skill page](https://clawhub.ai/kikidouloveme79/skills/senseaudio-voice-ab-lab)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON manifests, CSV review sheets, transcripts, and generated audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write synthesized MP3 variants, optional OGG/Opus Feishu delivery artifacts, variant metadata, ASR transcripts, and review exports.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
