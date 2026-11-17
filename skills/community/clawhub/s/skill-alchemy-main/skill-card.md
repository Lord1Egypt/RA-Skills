## Description:

Skill Alchemy Main orchestrates Lens and LEAP to turn a person, method, experience, or skill-fusion idea into an installable agent skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to plan, research, compile, and validate new installable skills or combinations of existing skills. It is intended for normal ClawHub release use, with human review before deploying generated skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may incorporate unreviewed public skill text or misleading guidance.

Mitigation: Review generated SKILL.md files, references, and scan results before installing or publishing them.

Risk: All-default generation can be too broad for sensitive targets.

Mitigation: Use explicit scope, depth, source requirements, and human checkpoints for sensitive people, methods, or domains.

Risk: The subtitle helper has weak input validation for untrusted or option-like input.

Mitigation: Do not run the subtitle helper on untrusted inputs, and pin installer or dependency versions where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsope/skills/skill-alchemy-main)
- [README_EN.md](artifact/README_EN.md)
- [SKILL.md](artifact/SKILL.md)
- [LEAP skill grammar](artifact/skills/LEAP/references/skill-grammar.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, structured task briefs, research plans, and generated SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a depth setting of quick, standard, or deep; generated skill artifacts are written under an output directory.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
