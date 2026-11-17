## Description:

把一家客户的一套税费材料按 5 项税费自查逐客户核一遍，每家客户一行结论，结论都带原文文件与行号，不需要付款、不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External tax accounting and bookkeeping users can run local post-filing self-checks across client folders to identify arithmetic and reconciliation issues in Chinese tax worksheets. The skill reports per-client conclusions and source file line references without replacing tax advice or official filing review.

### Deployment Geography for Use:

Global, for Chinese tax worksheet review workflows.

## Known Risks and Mitigations:

Risk: The skill reads tax worksheets and customer folders selected by the user.

Mitigation: Run it only on intended local folders and review folder contents before execution.

Risk: Clean results or passed checks may be mistaken for tax advice or official filing assurance.

Mitigation: Use the output as arithmetic and reconciliation evidence only, and consult a tax professional or tax authority for policy judgments.

Risk: Items marked not run, sub-checks not run, or insufficient input can be overlooked.

Mitigation: Review not-run statuses and missing-material messages before relying on any per-client conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-risk-benefit-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON summaries printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-client conclusions, finding severity counts, check status, and source file line references; does not write result files.]

## Skill Version(s):

1.0.21 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
