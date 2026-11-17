## Description:

通过 zwds-cli（Node、iztro 2.5.0）生成紫微斗数结构化命盘 JSON，并仅依据该 JSON 解盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Zi Wei Dou Shu chart JSON from birth time, gender, and location inputs, then produce readings grounded only in that JSON. It is suited for astrology chart generation and reflective interpretation, not professional medical, financial, legal, or relationship advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth time, gender, and location are sensitive personal inputs.

Mitigation: Use local execution where possible and avoid saving real personal chart fixtures in shared repositories or synced folders.

Risk: Longitude fallback or invalid location data can affect chart timing.

Mitigation: Validate longitude values and ask users to provide explicit decimal longitude for small, ambiguous, or unsupported places.

Risk: Astrology readings may be mistaken for professional health, finance, legal, or relationship advice.

Mitigation: Present readings as entertainment or reflection and direct users to qualified professionals for high-stakes decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luyao-inc/skills/zwds-openclaw)
- [iztro Quick Start](https://iztro.com/quick-start.html)
- [Skill Reference](artifact/reference.md)
- [Usage Examples](artifact/examples.md)
- [zwds-cli README](artifact/zwds-cli/README.md)
- [Administrative Divisions of China](https://github.com/modood/Administrative-divisions-of-China)
- [Aliyun DataV Boundary Data](https://geo.datav.aliyun.com/areas_v3/bound/{adcode}.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON from the chart CLI plus human-facing Markdown or text interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Readings should cite chart fields from the generated data and preserve warnings about default longitude or unsupported time layers.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
