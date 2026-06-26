## Description: <br>
Gives an OpenClaw agent a voice layer that can clone an authorized principal's voice with ElevenLabs, generate MP3 speech from text, and support conversational call workflows through Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add voice cloning, text-to-speech generation, call queue review, and lead-call workflow guidance to an OpenClaw agent. It is intended for authorized principal-voice use with configured ElevenLabs, Twilio, and Telegram credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate calls or voicemails using a cloned voice, which creates consent, disclosure, impersonation, and outreach-compliance risk. <br>
Mitigation: Use only voice samples with documented permission, disclose synthetic voice use at the start of calls and voicemails, keep opt-out lists, and confirm legal permission before outbound calling or SMS use. <br>
Risk: The skill sends text, audio, call data, and credentials to external ElevenLabs, Twilio, and Telegram services. <br>
Mitigation: Store credentials in a secret manager or locked-down environment, review what data is sent to each service, and define retention and deletion rules for samples, generated audio, transcripts, lead data, and cloned voices. <br>
Risk: Automated triggers such as cron jobs or cross-skill call triggers could start outreach before approval rules are clear. <br>
Mitigation: Avoid enabling scheduled or cross-skill call triggers until approval, working-hours, suppression-list, and escalation rules have been reviewed. <br>


## Reference(s): <br>
- [Voice Agent Pro ClawHub page](https://clawhub.ai/georges91560/voice-agent-pro-v1) <br>
- [Publisher profile](https://clawhub.ai/user/georges91560) <br>
- [Setup guide](artifact/setup_guide.md) <br>
- [ElevenLabs API target](https://api.elevenlabs.io) <br>
- [Twilio API target](https://api.twilio.com) <br>
- [Telegram Bot API target](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio files] <br>
**Output Format:** [Markdown guidance with shell and Python snippets; runtime outputs include MP3 files, JSON configuration, audit logs, and call records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided service credentials and authorized voice samples before voice cloning, text-to-speech, or call workflows can run.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
