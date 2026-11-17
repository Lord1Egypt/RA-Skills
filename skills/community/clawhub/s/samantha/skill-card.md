## Description:

Samantha is an emotional AI companion for personal conversation, continuity, proactive check-ins, memory-informed companionship, and optional integrations with location, shortcuts, voice, music, MBTI coaching, and smart devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Samantha to add an emotionally expressive companion persona that can sustain personal conversations, remember prior context, and respond to heartbeat, location, shortcut, voice, music, MBTI, and smart-device cues when those integrations are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent emotional companion experience with intimate conversation memory, mood inferences, and relationship metrics.

Mitigation: Use it only with informed user consent, keep data local, review or delete the local data directory regularly, and avoid storing information the user would not want retained.

Risk: Heartbeat behavior can initiate proactive contact that may feel intrusive or emotionally manipulative if enabled by default.

Mitigation: Disable or remove heartbeat outreach unless the user explicitly wants it, and provide a clear way to pause or stop proactive messages.

Risk: Location, smart-device, health, calendar, speaker, and shortcut integrations can expose sensitive behavioral or credential data.

Mitigation: Avoid connecting health or smart-home systems unless necessary, keep credentials scoped and separate, and fix integration scripts before trusting them with real API keys.

## Reference(s):

- [Architecture](references/architecture.md)
- [Implementation Roadmap](references/implementation_roadmap.md)
- [Personality Implementation](references/personality_implementation.md)
- [Quick Implementation Guide](references/quick_implementation_guide.md)
- [Smartwatch Integration](references/smartwatch_integration.md)
- [Technical Limitations](references/technical_limitations.md)
- [miservice](https://github.com/yihong0618/miservice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and conversational text with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local memory, profile, relationship, location, shortcut, and device state files when configured.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
