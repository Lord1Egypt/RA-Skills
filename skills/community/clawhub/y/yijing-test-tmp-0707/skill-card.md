## Description:

Pubtest provides Chinese I Ching divination analysis with six-line number decoding, hexagram text lookup, Zhu Xi and Nan Huaijin-style interpretation, daily-life guidance, and summary statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuzijun-nm](https://clawhub.ai/user/qiuzijun-nm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to perform culturally oriented I Ching readings from a six-digit input, retrieve bundled hexagram reference material, generate plain-language interpretation, provide eight-category daily-life guidance, and update local reading statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat health, wealth, or dispute readings as professional advice.

Mitigation: Present readings as cultural or entertainment-oriented interpretation and direct users to qualified professionals for medical, financial, legal, or safety-critical decisions.

Risk: Question topics and reading details may be saved into local log and statistics files.

Mitigation: Avoid entering sensitive personal information and review or clear local log/stat files before sharing the skill directory or outputs.

Risk: Bundled lookup data may have gaps, including a reported mismatch between the named 4096 table and the number of available entries.

Mitigation: Check lookup misses explicitly, disclose gaps to users, and avoid presenting missing-table results as authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuzijun-nm/skills/yijing-test-tmp-0707)
- [yijing-4096.csv](references/yijing-4096.csv)
- [yijing-full.csv](references/yijing-full.csv)
- [yijing-2026-calendar.csv](references/yijing-2026-calendar.csv)
- [yijing-log.csv](references/yijing-log.csv)
- [yijing-stats.json](references/yijing-stats.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown narrative with tables, plus local CSV and JSON record updates when logging is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled CSV/JSON reference data and may append local reading history and statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
