## Description:

Manage a Whop digital products store by creating products and plans, tracking payments, and managing memberships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and store operators use this skill to manage Whop digital product workflows through the Whop SDK, including product setup, pricing plans, payment review, and membership checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whop API keys and company identifiers are sensitive and could expose store-management access if leaked.

Mitigation: Use the least-privileged Whop API key available, keep credentials in environment or secret storage, and avoid committing or logging them.

Risk: The setup recommends a global unpinned npm installation for the Whop SDK.

Mitigation: Prefer a pinned project-local dependency before use in sensitive or repeatable environments.

Risk: Generated API examples can create or modify store resources such as products, plans, payments, and memberships.

Mitigation: Review proposed API calls and target company IDs before execution, especially for production stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/whop-cli)
- [Versatly Whop store](https://whop.com/versatly-holdings/)
- [Versatly products site](https://store.versatlygroup.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOP_API_KEY and WHOP_COMPANY_ID environment variables; examples use the Whop SDK.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
