## Description:

Provides entertainment-only Rider-Waite-Smith tarot readings for yes/no, advice, reminder, and lost-item questions in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafei0007](https://clawhub.ai/user/jiafei0007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce tarot-style entertainment readings, including card draws and interpretations for yes/no, advice, reminder, and lost-item prompts. It is intended for entertainment and should not be relied on for real-world decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tarot outputs may be mistaken for factual, professional, or decision-making advice.

Mitigation: Keep the entertainment-only framing visible and do not rely on readings for medical, legal, financial, safety, or other real-world decisions.

Risk: Broad trigger wording can route ordinary advice, yes/no, reminder, or lost-item requests into tarot readings.

Mitigation: Use the skill only when the user asks for or accepts a tarot-style entertainment response; otherwise provide ordinary assistance.

Risk: English readings may include Chinese card meanings.

Mitigation: Review bilingual output for clarity and translate or explain any Chinese terms when serving English-language users.

## Reference(s):

- [Card database](artifact/references/cards.py)
- [Chinese spread definitions](artifact/references/spreads.py)
- [English spread definitions](artifact/references/spreads_en.py)
- [ClawHub skill page](https://clawhub.ai/jiafei0007/skills/tarot-reading-new)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [JSON card-draw data plus formatted reading text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamp, spread, question type, language, drawn cards, orientations, meanings, and a concise entertainment-only interpretation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
