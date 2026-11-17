## Description:

Guides developers through TBC Bank Open Banking, PSD2, account information, payment initiation, installment, and TPay API integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erekle1](https://clawhub.ai/user/erekle1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand and implement TBC Bank API workflows for authentication, account information access, consent management, payment initiation, installments, and hosted payments. It is intended as integration guidance and example material, not production-ready banking code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers high-impact banking and payment workflows, including payment initiation, capture, cancel, void, consent revocation, and order fulfillment.

Mitigation: Require explicit user or operator confirmation before high-impact actions and verify payment, installment, or consent status through authenticated TBC Bank APIs before fulfilling or changing local records.

Risk: Callback examples may be unsafe if copied directly into production fulfillment logic.

Mitigation: Authenticate callbacks, verify signatures where applicable, compare amount, currency, order, and session data against local records, and make fulfillment idempotent.

Risk: The workflows involve sensitive credentials, tokens, private keys, account data, and payment data.

Mitigation: Protect credentials and tokens with appropriate secret storage, avoid logging sensitive banking data, and limit scopes to the minimum needed for each consent or payment flow.

## Reference(s):

- [TBC Bank API Integration Guide](artifact/SKILL.md)
- [TBC Bank Authentication & OAuth2](artifact/references/auth.md)
- [TBC Bank Account Information Services (AIS)](artifact/references/ais.md)
- [TBC Bank Consent Management & SCA](artifact/references/consent.md)
- [TBC Bank Payment Initiation Services (PIS)](artifact/references/pis.md)
- [TBC Bank Online Installments API](artifact/references/installments.md)
- [TBC Bank TPay Gateway](artifact/references/tpay.md)
- [TBC Bank Developer Portal](https://developers.tbcbank.ge)
- [ClawHub Skill Page](https://clawhub.ai/erekle1/skills/tbc-bank-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP, JSON, Python, JavaScript, and Ruby examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, headers, workflow steps, and security caveats for banking and payment integrations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
