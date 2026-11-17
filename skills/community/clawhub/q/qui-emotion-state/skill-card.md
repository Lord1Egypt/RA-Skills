## Description:

NL emotion tracking + prompt injection via OpenClaw hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and configure an OpenClaw bootstrap hook that classifies recent user and agent emotions, stores inferred emotion state, and injects a compact emotion summary into future agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation messages may be sent to an external or configured emotion classifier.

Mitigation: Enable the skill only where users understand that data flow, and prefer a trusted local or tightly controlled HTTPS classifier.

Risk: Emotion profiles persist on disk and may be injected into future prompts.

Mitigation: Define deletion and retention practices for stored emotion-state.json files before deployment.

Risk: Stored emotion profiles may be shared across agents when cross-agent entries are enabled.

Mitigation: Set EMOTION_MAX_OTHER_AGENTS to 0 unless cross-agent sharing is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-emotion-state)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and injected emotion_state text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The hook persists inferred emotion entries as JSON state and injects a compact emotion_state block during agent bootstrap.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
