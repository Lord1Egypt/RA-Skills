## Description: <br>
Use when a team wants to generate multiple ad, spoken-copy, sales, or promo voice variants from one typed or spoken creative brief, transcribe voice memos with AudioClaw ASR, and synthesize the variants with the same AudioClaw voice_id for A/B testing, regional wording experiments, or rapid commercial validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commercial, growth, sales, and content teams use this skill to turn typed briefs or spoken voice memos into multiple same-voice ad or promo variants for A/B review. The workflow supports ASR intake, structured brief extraction, copy variant generation, TTS synthesis, CSV review export, and optional Feishu audio delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign briefs, voice recordings, generated copy, synthesized audio, and metadata may be sent to AudioClaw/SenseAudio and, when enabled, Feishu. <br>
Mitigation: Use the skill only with data approved for those services, verify the Feishu destination before sending, and use least-privilege API and Feishu credentials. <br>
Risk: Feishu delivery and shared AudioClaw credential handling rely on helper code in the install tree. <br>
Mitigation: Review, trust, and pin the sibling Feishu helper and shared AudioClaw modules before enabling automatic audio delivery. <br>
Risk: Regional styles are wording adaptations and are not guaranteed dialect TTS. <br>
Mitigation: Treat regional variants as copy-testing candidates and review them with target-audience or language reviewers before launch. <br>


## Reference(s): <br>
- [AudioClaw ASR Brief Pipeline](references/asr_brief_pipeline.md) <br>
- [Commercial Voice A/B Patterns](references/commercial_ab_patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kikidouloveme79/senseaudio-voice-ab-lab) <br>
- [AudioClaw ASR API Endpoint](https://api.senseaudio.cn/v1/audio/transcriptions) <br>
- [AudioClaw TTS API Endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, CSV, audio files] <br>
**Output Format:** [Markdown guidance with Python commands, JSON manifests, CSV review sheets, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed voice_id across generated variants and can optionally send audio messages to Feishu.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
