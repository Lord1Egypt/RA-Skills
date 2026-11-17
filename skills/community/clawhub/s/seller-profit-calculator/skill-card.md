## Description:

Multi-platform order profit calculator that analyzes Excel order exports and produces profit reports by order, store, SKU, and platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and operators use this skill to inspect Excel order exports, map order fields, and calculate per-order and aggregate profit metrics for operational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order exports can contain customer data and business-sensitive revenue, cost, and profit columns.

Mitigation: Redact unnecessary customer or sensitive business columns before sharing files with an agent or running analysis.

Risk: The skill writes optional JSON and Markdown outputs to user-supplied paths.

Mitigation: Verify output paths before using --json or --markdown so reports are written only to intended locations.

Risk: The advertised hosted API/API key path is not implemented in the inspected parser.

Mitigation: Use the local Excel workflow unless hosted API behavior is separately verified.

Risk: The broad any-platform claim depends on exports containing recognizable order, revenue, cost, and profit fields.

Mitigation: Inspect headers first and provide an explicit field-map JSON when automatic column matching is incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiji0802/skills/seller-profit-calculator)
- [YK-Global website](https://yk-global.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report printed to stdout with optional JSON or Markdown output files and field-map JSON guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local Excel .xlsx and .xls order exports; output quality depends on recognizable revenue, cost, status, store, SKU, and platform fields.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
