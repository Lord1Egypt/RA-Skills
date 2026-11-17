## Description:

Checks Chinese stamp-duty tax-base ledgers for row-level arithmetic, total reconciliation, duplicates, and blank required fields, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and bookkeeping users run this skill before month-end, reconciliation, inventory checks, or stamp-duty filing work to review ledger consistency. It helps identify arithmetic mismatches, duplicate contract numbers, missing fields, and total-row discrepancies while leaving tax judgment and legal advice to qualified reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes Chinese-language stamp-duty ledger data and may be unsuitable for users who cannot review that domain-specific output.

Mitigation: Use it only when the reviewer understands the ledger format and can check findings against the original records.

Risk: The output is tax-assistance analysis, not legal or tax advice.

Mitigation: Have a qualified finance or tax reviewer confirm decisions before filing, payment, correction, or escalation.

Risk: The free edition intentionally omits several checks, including tax-rate matching, negative or zero contract amounts, overpayment checks, date parsing, and unreported-contract detection.

Mitigation: Treat clean results as limited to the listed free checks, and run additional review for omitted checks before relying on the ledger.

Risk: Insufficient or malformed input can prevent meaningful analysis.

Mitigation: Provide a ledger with the required headers and review any missing-field guidance instead of treating it as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/stamp-duty-base-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON findings from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each finding cites the relevant source row when the supplied ledger has enough required columns; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.55 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
