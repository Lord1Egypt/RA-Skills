## Description: <br>
Daily Stoic companion for personal growth and virtue tracking with affirmations, evening virtue check-ins, weekly summaries, and on-demand support for anxiety or impulsive moments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoklemariano](https://clawhub.ai/user/stoklemariano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal Stoic reflection companion for daily affirmations, evening journaling against the four cardinal virtues, weekly progress summaries, and short support flows during anxiety or impulse moments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive personal reflections, relationship context, and daily check-ins in memory. <br>
Mitigation: Record only details the user is comfortable retaining, and review or delete memory files when they are no longer needed. <br>
Risk: Scheduled messages or voice notes may be sent to the wrong recipient or channel if delivery settings are misconfigured. <br>
Mitigation: Verify the messaging channel, target ID, timezone, and schedule before enabling automated delivery. <br>
Risk: Optional TTS setup may require an external API key. <br>
Mitigation: Store the TTS API key securely and avoid exposing it in logs, prompts, shared configuration, or memory files. <br>
Risk: The skill offers reflective support during anxiety or impulse moments but is not professional or emergency mental-health care. <br>
Mitigation: Use it as coaching support only, and direct users showing deep distress to contact a therapist, qualified professional, or emergency service. <br>


## Reference(s): <br>
- [Stoic Companion configuration template](references/config-template.md) <br>
- [ClawHub Stoic Companion release page](https://clawhub.ai/stoklemariano/stoic-companion) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with configuration details, scheduled message content, and optional shell commands for audio delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce personalized journal entries, memory updates, cron schedules, and optional TTS-delivered affirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
