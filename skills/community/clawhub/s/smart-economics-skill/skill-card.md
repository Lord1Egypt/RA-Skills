## Description:

smart-economics-skill is a Chinese-language economics assistant that delivers daily concept prompts and reframes everyday financial, work, and consumption decisions through economics concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive Chinese-language daily economics concept prompts, ask for structured explanations, and get economics-based framing for everyday decisions about spending, debt, work, and investing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to create a daily recurring 08:00 task during installation without clear consent or removal controls.

Mitigation: Require explicit user consent before scheduling reminders and provide a clear way to pause, remove, or avoid duplicate scheduled tasks.

Risk: The skill may proactively reframe related user conversations through economics concepts.

Mitigation: Enable it only for users who want Chinese-language economics coaching and allow users to opt out of proactive reframing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/skills/smart-economics-skill)
- [Concept library](artifact/references/concepts.md)
- [Case library](artifact/references/cases.md)
- [Decision framework](artifact/references/decision-framework.md)
- [Daily queue](artifact/references/daily-queue.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown-style conversational responses and scheduled prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May proactively associate user conversations with economics concepts and may request a daily 08:00 recurring task if the host permits.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
