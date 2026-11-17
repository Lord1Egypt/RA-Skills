## Description:

Connects Xiaomi XiaoAi speaker voice messages to an AI assistant, filters commands, and replies with TTS; optionally sends transcripts to Jev for forwarding decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-winter](https://clawhub.ai/user/warm-winter)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and OpenClaw users can connect a Xiaomi XiaoAi speaker to an AI assistant for voice-driven tasks and smart-home workflows. They can configure keyword filtering or opt into Jev transcript-based forwarding decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence and reports partial inspection, so its findings do not establish that the skill is safe.

Mitigation: Review the full release and SECURITY.md guidance before installation, paying attention to persistent session state and files the scan did not inspect.

Risk: When JEV_API_KEY is configured, voice transcripts are sent to Jev for forwarding decisions.

Mitigation: Leave JEV_API_KEY unset unless sharing transcripts with Jev is acceptable; keyword-based forwarding remains available.

Risk: The skill uses Xiaomi login credentials and stores session state.

Mitigation: Keep credentials out of version control and use the private state directory and permission checks documented by the skill.

## Reference(s):

- [MI-GPT API reference](references/migpt-api.md)
- [mi-gpt-next repository](https://github.com/idootop/migpt-next)
- [Jev service](https://tokenrhythm.studio)
- [ClawHub release](https://clawhub.ai/warm-winter/skills/xiaoai-bridge)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON voice-message events and text for assistant or TTS replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live voice-message handling; transcript forwarding to Jev is optional and enabled by configuration.]

## Skill Version(s):

1.3.13 (source: frontmatter, CHANGELOG.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
