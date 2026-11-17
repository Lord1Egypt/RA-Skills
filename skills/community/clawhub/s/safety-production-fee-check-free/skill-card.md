## Description:

安全生产费用提取与使用核对表逐项核对，复算逐行金额、合计勾稽、重复与空缺，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business users in safety management and finance use this skill to check copied safety-production-fee tables before monthly close, fee extraction, or special-account reimbursement. It recalculates table arithmetic and flags duplicates, blanks, and negative values with source-line evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free-version result as a complete safety-production-fee compliance review even though several checks are explicitly not executed.

Mitigation: Review the executed and withheld check lists before relying on the output; use a complete review process for threshold, overspend, negative ending balance, zero extraction, and cumulative-use questions.

Risk: Chinese-language business and financial table data may be sensitive.

Mitigation: Use the skill only in an environment where local processing is acceptable; server security evidence reports no network use, persistence, credential access, or hidden behavior.

Risk: Missing or unrecognized table input can result in no conclusion rather than a clean result.

Mitigation: Provide a full table with headers and treat insufficient-input output as no opinion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/safety-production-fee-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; checker output is human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; the free version reports both executed and withheld checks.]

## Skill Version(s):

1.0.53 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
