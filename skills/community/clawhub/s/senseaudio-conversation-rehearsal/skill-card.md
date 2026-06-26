## Description: <br>
Use when a user wants to rehearse a high-pressure conversation such as a performance review, reporting meeting, promotion defense, difficult manager conversation, or stakeholder alignment session, using AudioClaw ASR for spoken rehearsal intake, AudioClaw TTS or an authorized cloned voice for the counterpart, and transcript-based debriefing on tone, structure, and communication risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, coaches, and communication-prep users use this skill to rehearse difficult workplace conversations with spoken counterpart turns, ASR-based intake, and transcript debriefs focused on tone, structure, evidence, and communication risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can be misused for impersonation or unauthorized rehearsal. <br>
Mitigation: Default to proxy voices; use cloned voices only with explicit sample-owner consent, a prepared authorized voice ID, and no impersonation or publishing. <br>
Risk: Spoken replies, transcripts, generated audio, and debriefs may contain sensitive HR, legal, or business information and can be sent to external ASR/TTS or messaging services. <br>
Mitigation: Use a local-only or explicitly confirmed mode for sensitive sessions, avoid confidential matters unless data handling is acceptable, and delete local output bundles when no longer needed. <br>
Risk: Credential handling includes API keys and optional browser-session token resolution. <br>
Mitigation: Use scoped API keys from a secret manager, avoid Chrome-session token extraction, and prefer explicit credentials with limited permissions. <br>
Risk: Feishu audio delivery can expose rehearsal content to the wrong chat or recipients. <br>
Mitigation: Confirm the target chat and recipient context before sending audio, and disable Feishu delivery for sensitive rehearsals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kikidouloveme79/senseaudio-conversation-rehearsal) <br>
- [Live Rehearsal Loop](references/live_rehearsal_loop.md) <br>
- [Rehearsal Design](references/rehearsal_design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON, text, and audio file artifacts from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use AudioClaw ASR/TTS, authorized clone voice IDs, Feishu audio delivery, and local session output bundles.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
