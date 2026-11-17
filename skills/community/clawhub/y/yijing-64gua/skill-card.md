## Description:

Provides I Ching 64-hexagram divination analysis with six-line number decoding, classical text lookup, Zhu Xi and Nan Huaijin style interpretations, everyday advice, and usage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuzijun-nm](https://clawhub.ai/user/qiuzijun-nm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate or interpret I Ching readings, look up the 64 hexagrams and line texts, and receive cultural-study oriented advice across everyday topics. Outputs should be treated as cultural interpretation rather than professional medical, legal, financial, or personal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep a local divination history, which may contain personal questions or sensitive context.

Mitigation: Avoid entering highly private details, disable or clean local logging when privacy matters, and review retained log files before sharing the artifact.

Risk: Reading subjects stored in CSV may be interpreted as formulas by spreadsheet software.

Mitigation: Neutralize formula-like user subjects before opening logs in spreadsheet tools.

Risk: Divination interpretations may be mistaken for professional advice.

Mitigation: Present outputs as cultural interpretation and direct users to qualified professionals for medical, legal, financial, or similarly high-stakes decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuzijun-nm/skills/yijing-64gua)
- [Publisher profile](https://clawhub.ai/user/qiuzijun-nm)
- [yijing-4096.csv](references/yijing-4096.csv)
- [yijing-full.csv](references/yijing-full.csv)
- [yijing-2026-calendar.csv](references/yijing-2026-calendar.csv)
- [yijing-log.csv](references/yijing-log.csv)
- [yijing-stats.json](references/yijing-stats.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown-style narrative with lookup tables and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include classical Chinese excerpts, plain-language interpretation, topic-specific advice, and local reading statistics.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
