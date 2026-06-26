## Description: <br>
A tarot reading and interpretation skill that draws from a 78-card Rider-Waite-Smith tarot deck and produces symbolic, reflective readings with spread-aware card meanings and action steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for entertainment-oriented tarot readings, daily card pulls, and reflective exploration of personal questions. It is intended for symbolic self-reflection and not for medical, legal, financial, or other professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional preference memory may retain sensitive personal reading topics if a user explicitly asks to save them. <br>
Mitigation: Avoid saving sensitive personal details as preferences and review MEMORY.md before reuse if past topics should not influence future readings. <br>
Risk: Broad trigger phrases such as 'daily card' or 'draw a card' may route an ambiguous request to this skill. <br>
Mitigation: Confirm the user's intent when the request is ambiguous or could refer to a non-tarot task. <br>
Risk: Users may over-rely on tarot output for professional, health, legal, or financial decisions. <br>
Mitigation: Keep readings framed as entertainment and self-reflection, and direct users to qualified professionals for medical, legal, financial, or other professional advice. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills) <br>
- [Tarot Interpretation Rules](references/interpretation-rules.md) <br>
- [Major Arcana](references/major-arcana.md) <br>
- [Minor Arcana](references/minor-arcana.md) <br>
- [Tarot Spread Reference](references/spreads.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tarot reading with drawn cards, card-by-card interpretation, synthesis, and action steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-selected or recommended spreads; card draws and upright/reversed orientation are randomized.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
