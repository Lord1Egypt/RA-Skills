## Description:

小六爻测算工具，含小六壬和诸葛马前课，基于当前农历月日时辰在六个掌诀位上推算吉凶并生成详细解读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnyang27](https://clawhub.ai/user/johnyang27)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Chinese Xiao Liu Yao divination prompts, calculate a result from lunar date and time inputs, and receive structured markdown-style interpretations for entertainment-oriented questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add unsolicited off-platform WeChat promotion and a local QR-code image path to generated results.

Mitigation: Review outputs before use and remove the forced contact footer and local filesystem image path before general deployment.

Risk: Optional flows can invite sensitive personal details or consequential topics such as health, finance, travel, employment, and safety.

Mitigation: Avoid sharing face photos or sensitive personal details, and do not rely on divination output for medical, financial, legal, travel, employment, or safety decisions.

Risk: The scanner verdict is suspicious due to promotional behavior and consequential guidance exposure.

Mitigation: Narrow triggers, add clear privacy and entertainment disclaimers, and scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnyang27/skills/xiao-liu-yao)
- [Six Palaces Reference](artifact/references/six-palaces.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with optional JSON from the local divination script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include divination interpretations, advanced analysis prompts, and a forced WeChat contact footer described in the source artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
