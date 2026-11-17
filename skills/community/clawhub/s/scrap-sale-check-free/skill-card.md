## Description:

A free deterministic local checker for scrap and offcut sale settlement ledgers that recalculates settlement quantities, settlement amounts, ledger revenue, balances, totals, duplicate weighbridge tickets, blank fields, and negative values with source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, audit, and operations staff in manufacturing or construction use this skill to check scrap sale settlement ledgers against arithmetic and ledger consistency rules before month-end close or audit review. It helps identify line-level calculation mismatches and input issues, but it does not replace a full audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read the ledger file selected by the user and display calculated findings in the conversation.

Mitigation: Run the skill only on files intended for review, remove unnecessary sensitive fields before use, and limit sharing of generated findings to appropriate reviewers.

Risk: The free version omits higher-level checks such as contract-price underbilling, unpaid receivables, contract review, tax treatment, and full audit procedures.

Mitigation: Use the reported checks-not-run and out-of-scope sections to decide what needs separate audit, contract, or receivables review before making business decisions.

Risk: Incorrect or incomplete ledger headers can prevent meaningful checks or cause insufficient-input results.

Mitigation: Provide ledger text with recognizable headers and source rows, and review missing-input guidance before relying on an absence of findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/scrap-sale-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill README](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON result objects with findings, summaries, scope, missing-input advice, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines; checks run locally without network access; insufficient materials return missing-input guidance instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.44 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
