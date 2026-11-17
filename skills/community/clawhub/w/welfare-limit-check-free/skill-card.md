## Description:

职工福利费与教育经费台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly closing, reconciliation, or review to check employee welfare and education expense ledgers for arithmetic, totals, duplicate rows, missing fields, and negative amounts. It is a limited free review and does not replace tax-compliance judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides a limited free ledger review, not a full tax-compliance opinion.

Mitigation: Use the findings as deterministic review cues and confirm tax treatment, filing choices, and adjustment timing against current rules or a qualified reviewer.

Risk: Several checks are explicitly outside the free version or outside the tool scope.

Mitigation: Review the omitted and out-of-scope checks before relying on the result; perform separate manual or complete-version checks for those areas.

Risk: Insufficient or malformed ledger input can prevent the skill from reaching a conclusion.

Mitigation: Provide the ledger with the required headers and source rows; treat an insufficient-input response as no conclusion rather than a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/welfare-limit-check-free)

## Skill Output:

**Output Type(s):** [analysis, JSON, markdown, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON validation report with cited ledger rows, executed checks, omitted checks, findings, and summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts a JSON file or pasted ledger text and can emit JSON with --json.]

## Skill Version(s):

1.0.46 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
