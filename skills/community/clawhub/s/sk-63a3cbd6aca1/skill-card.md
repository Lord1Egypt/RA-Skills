## Description:

魔杖选择你 is a Chinese-language entertainment skill that runs a local wand-matching quiz, generates a personalized wand card, and can compare two wand results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dora233](https://clawhub.ai/user/dora233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for a lightweight Chinese-language personality-style wand quiz, social sharing, and friend-to-friend result comparison. Agents can provide either a generated single-file quiz page or a text fallback that returns a complete wand card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python scripts and creates local HTML or PNG outputs.

Mitigation: Run it in an environment where local script execution and generated files are acceptable, and review generated files before distributing them.

Risk: Quiz cards include a reproducible answer string and tree identity intended for comparison with friends.

Mitigation: Review copied or shared cards first, and avoid sharing the reproducible string when users do not want others to compare or recreate the result.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dora233/skills/sk-63a3cbd6aca1)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated local HTML, text wand cards, and optional PNG artwork.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3; UI mode can generate a self-contained HTML quiz, and text mode returns reproducible wand-card output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
