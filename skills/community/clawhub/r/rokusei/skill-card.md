## Description:

Rokusei calculates a Six Star Astrology profile from a birth date, including star type, polarity, 12-year life cycle, destiny star, personality themes, compatibility, and sakkai warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikplpeter](https://clawhub.ai/user/ikplpeter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate entertainment-oriented Six Star Astrology readings from a birthday without requiring birth time. It can return human-readable profile guidance and optional JSON for agents that need structured astrology output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces fortune, health, career, and relationship statements that could be mistaken for professional advice.

Mitigation: Present outputs as entertainment only and avoid using them for medical, legal, financial, employment, or relationship decisions.

Risk: The CLI runs local Node.js code and installs an npm dependency.

Mitigation: Review the package files, install dependencies in a controlled environment, and run only from trusted release artifacts.

Risk: The skill asks for a birth date, which some users may treat as personal information.

Mitigation: Provide only the minimum date needed for the calculation and avoid sharing unnecessary identifying details.

## Reference(s):

- [ClawHub Rokusei Skill Page](https://clawhub.ai/ikplpeter/skills/rokusei)
- [Rokusei Online App](https://halfct.ltd/rokusei?lang=en)
- [lunar-typescript npm package tarball](https://registry.npmjs.org/lunar-typescript/-/lunar-typescript-1.8.6.tgz)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or terminal text with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses birthday input only; local CLI examples support language selection and a --json flag.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
