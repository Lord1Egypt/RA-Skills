## Description:

An information retrieval assistant for GaoKao score-by-score rankings, helping candidates query their provincial ranking based on their score, estimate the corresponding score range based on their ranking, or provide the complete score-by-score ranking table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhl-det](https://clawhub.ai/user/jhl-det)

### License/Terms of Use:

MIT-0

## Use Case:

Candidates and education advisors use this skill to look up Chinese GaoKao provincial score rankings, estimate score ranges from ranks, and retrieve score-by-score ranking tables for supported provinces, years, and subject categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a bundled Python script and queries Tencent's GaoKao service for lookup data.

Mitigation: Review the script before deployment and allow the external Tencent lookup only in environments where that dependency is acceptable.

Risk: The security guidance notes output-quality issues, including extra stdout prints that can make strict JSON parsing unreliable.

Mitigation: Treat script output as mixed diagnostic text plus JSON until the publisher fixes the extra prints, or normalize the output before automated consumption.

Risk: The security guidance identifies a misnamed --ip argument whose behavior is unclear.

Mitigation: Avoid using --ip unless the publisher documents or removes it; use the documented --place argument for province selection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhl-det/skills/score-range)
- [Tencent GaoKao lookup data endpoint](https://gaokao.search.qq.com/skills_data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise natural-language answers with supporting JSON lookup results from the bundled script when data is queried.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a bundled Python script that queries Tencent's GaoKao service for score/rank data.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
