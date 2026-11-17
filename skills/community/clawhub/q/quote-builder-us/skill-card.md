## Description:

Builds a US customer quote with line items, sales tax treatment, margin and total, and a stated validity date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US sales teams and small businesses use the skill to prepare written customer quotes with line items, tax treatment, margin, totals, and a validity date.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The supplied quote template and calculation workflow need correction, so amounts, tax, margin, or quote validity may be inaccurate.

Mitigation: Correct the template/script mismatch and independently verify all figures, applicable tax, margin, and expiration before sending a quote.

Risk: Generating another estimate in the same output folder overwrites estimate.md.

Mitigation: Use a dedicated output folder for each estimate and retain the reviewed quote with the deal record.

Risk: The optional Windows executable is unsigned, and its published hash does not establish that it is safe.

Mitigation: The executable is unnecessary for the Python workflow; make a separate trust decision before downloading or running it.

## Reference(s):

- [US quote, tax and price advertising rules](artifact/references/us-quote-rules.md)
- [US Quote Builder on ClawHub](https://clawhub.ai/rapidworker1/skills/quote-builder-us)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown estimate report (estimate.md)]

**Output Parameters:** [Line items, amounts, sales tax, margin, currency, and quote validity details]

**Other Properties Related to Output:** [Written to the selected output folder; an existing estimate.md is overwritten.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
