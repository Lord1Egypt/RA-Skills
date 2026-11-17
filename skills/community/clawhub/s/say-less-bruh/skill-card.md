## Description:

Use when the user explicitly asks for shorter, more human responses with minimal formatting, usually by saying "Say Less Bruh" or asking for shorter replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakeacp](https://clawhub.ai/user/jakeacp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent respond in shorter, more natural messages while preserving critical warnings, blockers, and key facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Short-answer mode can compress responses enough that important nuance is lost.

Mitigation: Preserve warnings, blockers, irreversible-risk notes, and key facts, and exceed the target length when needed for correctness.

Risk: The mode can keep responses brief for the rest of a conversation after activation.

Mitigation: Allow clear user instructions such as "Disable SLB", "turn off SLB", or "full response" to deactivate the mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jakeacp/skills/say-less-bruh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Short natural-language replies with minimal formatting; exact code, shell commands, JSON, YAML, and configuration blocks may remain as long as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefixes normal user-facing replies with "SLB: " while active and allows longer answers when brevity would omit critical details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
