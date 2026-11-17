## Description:

Builds a line-item US roofing estimate with tear-off, decking, flashing, waste and labor, plus the notice and deposit terms the state requires. Use when the user asks for roofing estimate template, roof replacement estimate, roofing bid sheet us. For US residential roofing contractors and the production managers who write their bids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External US residential roofing contractors and production managers use the skill to prepare line-item roof estimates, change-order triggers, deposit terms, notices, and open items from job details and field measurements.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Implementation gaps, including CSV/YAML input and missing-template issues, can make generated estimates incomplete or unreliable; prices and jurisdiction-specific terms may also be incorrect.

Mitigation: Resolve the input and template issues, then verify measurements, prices, and state/local notices, permits, and contract terms before relying on or sharing an estimate.

Risk: The optional Windows app is separate, unsigned, and not reviewed by the supplied security assessment.

Mitigation: Use the bundled workflow without the app; independently review the Windows download before running it, and do not treat its published hash as proof of safety.

## Reference(s):

- [Roofing contract rules](references/roofing-contract-rules.md)
- [Publisher homepage (skill metadata)](https://github.com/rapidworker1)
- [ClawHub skill listing](https://clawhub.ai/rapidworker1/skills/roofing-estimate-builder)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown roofing estimate with line items, change-order triggers, deposit terms, notices, and open items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimate details must be based on contractor-provided measurements and reviewed before customer use.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
