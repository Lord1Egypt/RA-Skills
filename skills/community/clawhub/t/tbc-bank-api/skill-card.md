## Description: <br>
Provides reference guidance for building integrations with TBC Bank's Open Banking, PSD2, account information, payment initiation, installments, and TPay APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erekle1](https://clawhub.ai/user/erekle1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when implementing or reviewing TBC Bank integrations for OAuth2, consent and SCA, account information, payment initiation, merchant installments, and TPay checkout flows. <br>

### Deployment Geography for Use: <br>
Georgia <br>

## Known Risks and Mitigations: <br>
Risk: Banking API examples may be incomplete or unsafe if copied directly into production financial integrations. <br>
Mitigation: Verify all flows against official TBC Bank documentation and require human review before enabling real account access, payments, or order fulfillment. <br>
Risk: Payment, installment, and callback workflows can create financial or fulfillment errors if status, signature, idempotency, or replay handling is missing. <br>
Mitigation: Implement callback signature or status verification, idempotency controls, replay protection, sandbox/live separation, and reconciliation before production use. <br>
Risk: OAuth credentials, access tokens, consent identifiers, and merchant secrets are sensitive financial integration data. <br>
Mitigation: Use secure secret storage, least-privilege access, proper OAuth consent handling, and environment-specific credentials. <br>


## Reference(s): <br>
- [TBC Bank Authentication and OAuth2](references/auth.md) <br>
- [TBC Bank Account Information Services](references/ais.md) <br>
- [TBC Bank Payment Initiation Services](references/pis.md) <br>
- [TBC Bank Consent Management and SCA](references/consent.md) <br>
- [TBC Bank Online Installments API](references/installments.md) <br>
- [TBC Bank TPay Gateway](references/tpay.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, Python, JavaScript, and Ruby examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference material only; users must verify production banking flows against official TBC Bank documentation.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
