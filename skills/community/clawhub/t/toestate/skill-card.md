## Description:

查台灣實價登錄、特定社區或建案房價、開價與附近成交比較、租金、行政區趨勢、法拍點交、地號與使用分區、交屋供給或自住預算時使用。也適用於使用者直接指定 ToEstate。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

台灣的購屋者、租屋者及房產研究者可用此技能查詢公開的不動產成交、租金、區域趨勢、土地與法拍資料，並整理附有來源與查詢範圍說明的比較結果。

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: Property details such as an address, asking price, area, and parking information may be sent to an external service without a privacy disclosure.

Mitigation: Send only the fields needed for the requested lookup; omit names and private notes, and use an administrative area or road segment instead of a full address when that is sufficient.

## Reference(s):

- [ToEstate via mcporter workflow](artifact/references/mcporter-workflow.md)
- [Property research workflows](artifact/references/property-workflows.md)
- [ToEstate tool catalog](artifact/references/tool-catalog.md)
- [ToEstate MCP guide](https://toestate.tw/mcp-guide)
- [ToEstate official data index](https://toestate.tw/llms.txt)
- [ToEstate on ClawHub](https://clawhub.ai/wei840222/skills/toestate)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance, Shell commands]

**Output Format:** [Markdown summaries with source attribution, query scope, dates, and sample counts; Bash commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports data coverage and interpretation limits; comparisons are not appraisals or bid recommendations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
