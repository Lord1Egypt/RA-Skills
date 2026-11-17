## Description:

Pricing Engine calculates B2B product quotes using LME copper price data, quantity tiers, customer grades, exchange rates, and quotation workflow integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill through an agent to calculate single-SKU or batch B2B quotes, apply customer-specific pricing rules, preview totals, generate quotation files, and query quote history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate business quote files without enforcing the claimed approval hold for below-floor-margin quotes.

Mitigation: Review and patch the quotation workflow so pending_approval blocks file generation or external sending until an authorized approval is recorded.

Risk: The quotation integration uses an environment-controlled workflow path in shell command execution.

Mitigation: Replace shell execution with execFile or spawn, validate configured paths against an allowlist, and run only in a controlled environment.

Risk: Generated quotation files and price-history JSONL records may contain sensitive commercial pricing and customer data.

Mitigation: Apply access controls, retention rules, and review procedures for generated output and history files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cjboy007/skills/ssa-pricing-engine)
- [Exchange-rate API endpoint used by the skill](https://open.er-api.com/v6/latest/USD)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON pricing results and generated quotation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote history is stored as JSONL when enabled by the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
