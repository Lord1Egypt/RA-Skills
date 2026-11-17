## Description:

SBTI runs a Chinese-language parody personality quiz that asks humorous questions, scores answers across four fictional dimensions, and produces an intentionally unserious personality result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for a lighthearted Chinese-language personality test. The agent asks ten randomized questions, tracks fictional C/S/E/W scores, and returns a humorous result card with traits and compatibility notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the parody personality result for a scientific or psychological assessment.

Mitigation: Keep the humorous framing and no-scientific-basis disclaimer visible in the quiz flow and result card.

Risk: The skill may activate on fairly general personality-test wording.

Mitigation: Use it when the user asks for SBTI or a playful personality quiz, and clarify the parody scope when intent is ambiguous.

## Reference(s):

- [SBTI question bank](artifact/references/questions.md)
- [SBTI personality types](artifact/references/types.md)
- [ClawHub skill page](https://clawhub.ai/enihsago/skills/sbti-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese conversational quiz prompts and a Markdown-style result card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Randomized 10-question flow; no code execution, credential access, persistence, or hidden data flow reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
