## Description:

This skill helps agents analyze Chinese relationship-language patterns associated with emotional manipulation, using five cognitive models and eight decision heuristics distilled from 403 dialogue examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjiang1989](https://clawhub.ai/user/dongjiang1989)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to classify quoted Chinese relationship statements, explain manipulative patterns, and suggest defensive responses. Its analysis should be treated as pattern-recognition guidance, not a diagnosis or a substitute for professional support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may route sensitive relationship discussions into this framework.

Mitigation: Use the skill only for Chinese-context relationship-language analysis and confirm that the user wants this framing before applying it to sensitive personal situations.

Risk: Users may over-read pattern matches as a diagnosis of a person or relationship.

Mitigation: Frame outputs as language-pattern analysis, include uncertainty where context is limited, and direct abuse or mental-health concerns to qualified professional support.

Risk: The skill can simulate manipulative phrasing when explicitly asked.

Mitigation: Clearly label any simulation as an example for recognition or education and pair it with defensive interpretation rather than operational advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongjiang1989/skills/scumbag)
- [Artifact README](README.md)
- [Skill definition](SKILL.md)
- [Extraction framework](references/extraction-framework.md)
- [Quotation system analysis](references/research/01-writings.md)
- [Conversation-pattern analysis](references/research/02-conversations.md)
- [Expression DNA analysis](references/research/03-expression-dna.md)
- [External-view analysis](references/research/04-external-views.md)
- [Decision-pattern analysis](references/research/05-decisions.md)
- [Timeline analysis](references/research/06-timeline.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style narrative analysis with classification, quoted-text breakdown, defensive guidance, and a qualitative risk level]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clearly labeled simulated manipulative phrasing when the user explicitly requests a simulation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
