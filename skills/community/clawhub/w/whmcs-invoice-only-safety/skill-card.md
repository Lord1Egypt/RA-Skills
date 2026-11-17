## Description:

Use when building or reviewing an authorized WHMCS invoice-only order adapter that creates an unpaid invoice and never takes payment. Covers pinned-product preconditions, login/cart verification, checkout field discipline, single-submit semantics, and post-submit invoice validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build or review authorized WHMCS/Lagom automation that creates and validates an unpaid invoice while avoiding accidental payment or unintended order changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating an unpaid invoice still creates an order record.

Mitigation: Authorize the exact product and final submission before use.

Risk: Credentials or unsafe adapter behavior could undermine the stated safeguards.

Mitigation: Protect the password file and verify the actual adapter implements these safeguards; review the referenced testing skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xinian5216/skills/whmcs-invoice-only-safety)
- [Publisher profile](https://clawhub.ai/user/xinian5216)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with implementation guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the supplied WHMCS/Lagom ordering workflow.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
