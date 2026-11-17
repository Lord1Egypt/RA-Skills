## Description:

校外培训机构资质与教师备案台账逐项核对（免费版执行 6 项免费检查项，含证照有效期覆盖、教师持证与备案、收费是否进监管账户、同一教师重复登记与证号跨主体、合计行逐列复核、字段合法性），逐行复算并引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

校外培训机构校区负责人、教务、财务或合规人员用它在每月自查和教育局年检前核对资质与教师备案台账。它 reports line-cited findings for the free checks and withholds conclusions when required ledger material is missing.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The checker processes potentially sensitive institutional ledger data.

Mitigation: Run it only in an environment approved for those records; evidence.security reports no hidden network behavior, and artifact behavior states execution is local.

Risk: The skill does not verify official certificate authenticity or replace regulator review.

Mitigation: Use findings as ledger-check support and confirm license, teacher, account, and local regulatory questions with the relevant authorities.

Risk: Missing or malformed ledger fields can produce unsupported conclusions if treated casually.

Mitigation: Rely on the tool's insufficient_input result and provide the required columns before acting on a conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/training-institution-license-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal output or JSON with findings, summary, executed checks, withheld checks, and scope notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts a JSON or pasted text ledger input up to 4 MB; returns insufficient_input instead of conclusions when required fields are missing.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
