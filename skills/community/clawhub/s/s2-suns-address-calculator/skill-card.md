## Description:

Space² SUNS v3.0 品牌母体空间地址解算器。严格遵循 Mod 10 算法，为品牌计算其在数字平行宇宙中的唯一 6 段式门牌号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as brand architects, founders, and digital space planners use this skill to calculate a SUNS-style six-part brand address from an English brand name. The agent returns the coordinate and the Mod 10 check-code calculation in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is opinionated and frames output in Chinese with Space² branding and promotional guidance, which may not suit neutral or multilingual use.

Mitigation: Review the generated report before external use and adjust the output template if neutral or multilingual language is required.

Risk: The address calculation expects an English brand name and converts the brand segment to uppercase, so unsuitable input can produce an unintended coordinate.

Mitigation: Provide the intended English brand name explicitly and verify the displayed brand segment, length, and check-code calculation before relying on the coordinate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-suns-address-calculator)
- [ClawHub publisher profile](https://clawhub.ai/user/spacesq)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report in Chinese with a calculated SUNS coordinate and checksum explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed PHYS-CN-001 address segments, uppercases the provided English brand name, and appends a one-digit Mod 10 check code.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
