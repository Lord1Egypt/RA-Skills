## Description:

Tamper-evident payment ledger for autonomous agents - auto-detects payments across tools, prevents duplicate payments, and presents spending history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattpolly](https://clawhub.ai/user/mattpolly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Spend Ledger to track autonomous-agent payments, review spending by service or time period, verify ledger integrity, and reduce duplicate payment risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic hooks can observe tool calls and persist spending and request metadata.

Mitigation: Review before installing, avoid exposing sensitive prompts in payment metadata, and use only where a local payment ledger is acceptable.

Risk: Duplicate-looking payment calls may be blocked, which can affect agent behavior.

Mitigation: Review blocked transactions with the ledger query tools and confirm any intended repeat payment before proceeding.

Risk: The localhost dashboard has review-worthy risk around transaction data exposure until authentication, CSRF protection, and stored-XSS fixes are present.

Mitigation: Do not run the dashboard while browsing untrusted sites; keep it local and stop it when review is complete.

Risk: Community pattern sync downloads payment detection patterns daily.

Mitigation: Set sync_community_patterns to false when offline or pre-reviewed behavior is required.

## Reference(s):

- [Spend Ledger on ClawHub](https://clawhub.ai/mattpolly/skills/spend-ledger)
- [Spend Ledger Homepage](https://spend-ledger.com)
- [Technical Architecture](TECHNICAL.md)
- [Payment Tool Signatures](references/payment-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance, shell command output, configuration JSON, and local JSONL ledger records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local transaction files and can present spending through a localhost dashboard.]

## Skill Version(s):

0.4.0 (source: SKILL.md frontmatter, openclaw.plugin.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
