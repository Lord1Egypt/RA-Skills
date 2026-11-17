## Description:

Checks Chinese or bilingual trade documents for cross-document mismatches in invoice, contract, letter-of-credit, amount, quantity, weight, port, vessel, shipping-mark, and placeholder fields, with original-text evidence in each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External trade operations staff and developers use this skill before document submission to identify inconsistent fields across invoices, packing lists, bills of lading, and related trade documents. It is a pre-check for supported consistency issues, not a bank, legal, or letter-of-credit acceptance decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result may be mistaken for bank, legal, or letter-of-credit assurance.

Mitigation: Use the output as a supported-field consistency pre-check only, and have qualified staff review bank requirements, legal terms, and LC conditions before relying on the documents.

Risk: The free version omits deeper checks such as line-item arithmetic, total recalculation, date ordering, LC limits, document-copy counts, and certificate or insurance cross-checks.

Mitigation: Run separate review steps for omitted categories before submission, especially where financial exposure or bank discrepancy fees are material.

Risk: The checker can only compare fields it extracts from supplied Chinese or bilingual trade-document text.

Mitigation: Provide complete document text in the documented input formats and manually inspect fields that are absent, malformed, or outside the supported labels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/trade-doc-consistency-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Human-readable text or JSON containing findings, quoted evidence, executed scope, withheld scope, and status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish completed checks, missing input, insufficient materials, unreadable or unparsable input, and unexpected errors.]

## Skill Version(s):

1.0.52 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
