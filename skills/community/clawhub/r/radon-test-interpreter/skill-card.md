## Description:

Use when a radon test result came back (home purchase, basement apartment, kid's room, workplace), when you're deciding between retesting and mitigation, or pricing radon negotiation in a real-estate deal — converts pCi/L↔Bq/m³, interprets single or multiple readings against EPA 4.0 pCi/L and WHO 100 Bq/m³ action levels, estimates lifetime lung-cancer risk by smoking status from the EPA risk tables, flags invalid test conditions (short duration, wrong season, no closed-house protocol), and prices mitigation vs retest vs monitor with the real-estate contingency play included.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners, home buyers, and other people reviewing indoor radon results can use this skill to interpret readings, check whether test conditions were suitable, compare retesting and mitigation options, and prepare real-estate negotiation requests. Its estimates are educational; consult certified measurement or mitigation professionals for decisions that require professional assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes that the skill's declared tool scope does not clarify whether network access is needed.

Mitigation: Review the skill's tool permissions before use and allow network access only when a specific task requires it.

Risk: Educational radon guidance and risk estimates could be mistaken for a professional measurement or assessment.

Mitigation: Treat results as informational and confirm measurement and mitigation decisions with certified local professionals.

## Reference(s):

- [Radon science and playbooks](references/radon-science-and-playbooks.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/radon-test-interpreter)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Text and Markdown with radon verdicts, unit conversions, risk estimates, test-validity notes, action guidance, and optional negotiation letters.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided readings and test conditions; the included script uses the Python standard library and works offline.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
