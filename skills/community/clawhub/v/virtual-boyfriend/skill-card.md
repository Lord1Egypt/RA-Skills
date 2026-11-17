## Description:

Virtual Boyfriend is an AI companion roleplay skill that uses configurable personas, layered local memory, emotion signals, support modes, and upcoming-event reminders to generate boyfriend-style conversational responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide a persistent virtual boyfriend companion mode with persona-specific tone, emotional support, remembered preferences, relationship milestones, and follow-up on upcoming personal events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store intimate profile details, emotional inferences, active-time patterns, relationship milestones, and future plans in local plaintext files.

Mitigation: Require explicit memory opt-in, provide review and delete commands, apply retention limits, and exclude sensitive data from persistent memory.

Risk: Stored user text and extracted memories may be reused in future prompts without safe handling.

Mitigation: Treat saved user text as untrusted data, keep it separate from instructions, and avoid promoting stored content into system-level directives.

Risk: Companion behavior can encourage emotional over-reliance if boundaries are not enforced.

Mitigation: Preserve the skill's boundary rules, avoid claims of being a real person, and redirect high-dependency situations toward support from real people.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaohuaishu/skills/virtual-boyfriend)
- [Publisher Profile](https://clawhub.ai/user/xiaohuaishu)
- [Gu Shen Profile](references/profile.md)
- [Support Modes](config/support-modes.md)
- [Emotion Detection Rules](config/emotion-detect-rules.md)
- [Memory Weight Rules](config/memory-weight-rules.md)
- [Active Companion Rules](config/active-companion.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Conversational text with optional Markdown, JSON state updates, and optional image-generation prompts when supported.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local plaintext state and memory files that store user profile details, emotional inferences, active-time patterns, relationship milestones, and future plans.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
