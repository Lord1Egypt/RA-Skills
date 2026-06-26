## Description: <br>
Instant EU VAT validation with Lightning Bitcoin. 10 sats per lookup. No subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcclawd](https://clawhub.ai/user/mcclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to request EU VAT number validation, pay a small Lightning invoice, and retrieve company validity details. It is intended for pay-per-use VAT lookup workflows that can tolerate external payment and VAT API calls. <br>

### Deployment Geography for Use: <br>
Global, for EU VAT numbers <br>

## Known Risks and Mitigations: <br>
Risk: VAT numbers and payment metadata may be sent to external VAT, n8n, BTCPay, and Lightning-related services. <br>
Mitigation: Use trusted HTTPS endpoints, avoid production secrets during testing, and make users aware of which services receive VAT and payment metadata. <br>
Risk: The skill can create Lightning payment requests and may use wallet credentials for automated payment flows. <br>
Mitigation: Use least-privileged wallet credentials, verify invoice details before payment, and keep automatic payment disabled unless the workflow has been tested. <br>
Risk: Artifact notes identify unresolved status endpoint and payment webhook issues in the soft-launch workflow. <br>
Mitigation: Run an end-to-end validation with a real payment and confirm status and payment webhooks before depending on automated completion. <br>
Risk: API tokens and wallet identifiers may be required for auto-pay or service integrations. <br>
Mitigation: Store credentials outside source files, scope them narrowly, and rotate or revoke them if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcclawd/vatgentic) <br>
- [VatGentic Documentation](https://docs.vatgentic.com) <br>
- [VatGentic Status](https://status.vatgentic.com) <br>
- [ln.bot API](https://api.ln.bot) <br>
- [EU VAT API](https://eu.vatapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured VATGENTIC_API_URL and optional Lightning wallet credentials; validation results depend on external VAT and payment services.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
