## Description:

二次供水清洗消毒与水质检测台账逐项核对（免费版执行 6 项免费检查项，含 180 天清洗周期、常规指标齐全与限值判定、清洗单位与健康证覆盖、重复清洗、合计勾稽、字段合法性），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

物业公司、供水管理单位、写字楼商业综合体、学校和医院后勤团队用它复核二次供水清洗消毒与水质检测台账。它检查清洗周期、检测项目和限值、清洗单位与健康证覆盖、重复清洗记录、合计行和字段合法性，并在结论中引用原文行号。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can flag ledger inconsistencies, but it does not verify real-world certificate authenticity or replace regulatory review.

Mitigation: Use its findings as a local ledger review aid and confirm certificate validity, laboratory report validity, and regulatory conclusions through the responsible authority or qualified reviewer.

Risk: The built-in guidance is primarily Chinese and specific to secondary water supply records.

Mitigation: Deploy it only for teams that can review Chinese secondary water supply ledgers and understand the local recordkeeping context.

Risk: It runs a local Node.js script on ledger text supplied by the user.

Mitigation: Install and run it only in an environment where local execution of this package on the provided ledger data is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/secondary-water-supply-check-free)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/scripts/run.mjs](artifact/scripts/run.mjs)
- [artifact/templates/sample.json](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON results with cited source lines and omitted-check notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; requires user-provided ledger text or JSON input.]

## Skill Version(s):

1.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
