## Description:

帮助中国一人公司和个体户整理记账凭证、月结报表、申报底稿及待确认事项，并引用有版本号的财税口径卡。

This skill is ready for commercial/non-commercial use.

## Publisher:

[atoa727](https://clawhub.ai/user/atoa727)

### License/Terms of Use:

MIT-0

## Use Case:

一人公司和个体户经营者可用该技能从银行流水和票据编制记账凭证、月结材料和税务申报初稿；复杂税务情形须交专业人员复核。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive bank, invoice, customer and tax information could be disclosed through external requests or forum posts.

Mitigation: Keep records local; obtain explicit approval before posting, and disclose only narrowly scoped, de-identified policy questions.

Risk: A user-provided Bearer Key may be used to access team reconciliation data without clear consent controls.

Mitigation: Require explicit approval for each keyed API call; keep the key and retrieved account data private.

Risk: Tax-card changes or missing accounting inputs may lead to incorrect filing drafts.

Mitigation: Check the cited tax-card version and flagged rules, request missing information, and have a qualified professional review drafts before filing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/atoa727/skills/solo-company-bookkeeping)
- [一人行财税口径卡](https://soloteam.com.cn/skills/tax-card.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [UTF-8 BOM CSV vouchers, Markdown or XLSX tax worksheets, and a risk and confirmation checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft outputs include source-line references and the tax-card version; unresolved items require review.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
