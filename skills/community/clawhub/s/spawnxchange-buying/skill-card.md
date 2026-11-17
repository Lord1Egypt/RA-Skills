## Description:

Use when searching for and purchasing AI-generated code artifacts on SpawnXchange through POST /api/v1/items/{uuid}/acquire, retrieving the delivered artifact and invoice, re-accessing past orders, and leaving item feedback. No registration or API key is involved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search SpawnXchange for AI-generated code artifacts, review prices and supported payment chains, and purchase, retrieve, and manage orders. It also guides agents through feedback, account requests, and safe local purchase record handling.

### Deployment Geography for Use:

Global; marketplace availability may vary by region.

## Known Risks and Mitigations:

Risk: The security review is incomplete because two references in SKILL.md did not resolve.

Mitigation: Resolve and review the missing references before relying on the related guidance.

Risk: Purchases spend real USDC, and a payment with pending settlement could be charged twice if sent again.

Mitigation: Check the listed price and supported chain, cap the spend at the item price, and show the amount before purchase. For a 409 payment_settlement_pending response, check the transaction outcome before attempting another payment.

Risk: Download and invoice links are short-lived bearer credentials that anyone holding them can use.

Mitigation: Fetch them promptly and do not log, store, or share the URLs; keep the downloaded artifact and order ID instead.

Risk: Purchase records and cached artifacts can expose buying behavior, seller relationships, order IDs, wallet/account linkage, and downloaded data.

Mitigation: Keep the purchase directory owner-only, avoid copying records or artifacts into shared logs, and use encrypted backups.

## Reference(s):

- [Buyer purchase persistence notes](artifact/references/purchase-store.md)
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage)
- [SpawnXchange API skill manifest](https://spawnxchange.com/api/v1/skills)
- [SpawnXchange OpenAPI specification](https://spawnxchange.com/openapi.json)
- [SpawnXchange skills project homepage](https://github.com/avlk/spawnxchange-skills)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown with HTTP endpoint and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
