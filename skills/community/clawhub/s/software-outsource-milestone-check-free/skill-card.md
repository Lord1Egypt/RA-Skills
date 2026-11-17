## Description:

软件外包里程碑验收与付款核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, project operations, and outsourcing payment reviewers use this skill before monthly settlement or payment review to check software outsourcing milestone acceptance and payment tables. It recomputes free-tier arithmetic and consistency checks, cites source lines, and reports missing material instead of inventing conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node.js script on payment-table content.

Mitigation: Install and run it only where local processing of the provided payment data is acceptable; use the sample mode first and keep sensitive inputs in the local execution environment.

Risk: The free version omits several full review checks, including overpayment beyond contract total, acceptance-payment conflicts, retention mismatch, payment-ratio completeness, and duplicate milestone payment detection.

Mitigation: Treat results as free-tier table checks only and separately review contract terms, acceptance records, retention treatment, approval status, and any withheld checks before payment decisions.

Risk: The interface and findings are mainly in Chinese.

Mitigation: Have a Chinese-literate reviewer validate findings and use JSON output when structured downstream review or translation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/software-outsource-milestone-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Chinese human-readable text or structured JSON findings from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local execution; accepts a JSON file or pasted payment-table text; reports executed checks, withheld checks, findings, summary, and out-of-scope items.]

## Skill Version(s):

1.0.51 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
