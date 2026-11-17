## Description:

Zan Gongde lets OpenClaw users intentionally consume remaining plan tokens by repeatedly prompting the configured LLM, with user-visible, silent, TTS, and high-concurrency modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jageri](https://clawhub.ai/user/jageri)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to spend unused token quota through automated Buddhist-recitation prompts, including faster high-concurrency token consumption when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally spends OpenClaw tokens and can unexpectedly deplete quota.

Mitigation: Install and run it only when deliberate token consumption is desired; start with low token targets and monitor account usage.

Risk: The high-concurrency mode lacks firm limits and reliable stopping controls.

Mitigation: Avoid high-concurrency runs unless budget and rate-limit approval are explicit, and keep worker counts conservative.

Risk: Token estimates and documented stop controls are not hard safeguards.

Mitigation: Treat displayed counts as estimates and enforce spending limits outside the skill through account or platform controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jageri/skills/zan-gongde)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown progress updates and generated LLM responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode, token target, and worker count influence response volume, concurrency, and token spend.]

## Skill Version(s):

2.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
