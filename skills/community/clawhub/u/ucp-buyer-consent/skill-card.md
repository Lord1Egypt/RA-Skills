## Description: <br>
Implement the UCP Buyer Consent extension for GDPR/CCPA consent collection, checkout-session consent fields, and privacy-compliant consent management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichiorca](https://clawhub.ai/user/ichiorca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add human-in-the-loop buyer consent flows to UCP checkout sessions for analytics, preferences, marketing, and sale-of-data choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated implementation guidance may rely on stale UCP details. <br>
Mitigation: Confirm the live UCP Buyer Consent specification before implementing fields or schemas. <br>
Risk: Consent decisions could be applied without the buyer's explicit approval. <br>
Mitigation: Keep consent choices human-approved and avoid auto-granting consent through the agent. <br>
Risk: Stored consent records contain privacy-relevant user data. <br>
Mitigation: Protect consent records, include timestamps for auditability, and support withdrawal workflows where required. <br>
Risk: Third-party examples may be copied without review. <br>
Mitigation: Review external samples against the live UCP specification and local compliance requirements before use. <br>


## Reference(s): <br>
- [UCP Buyer Consent specification](https://ucp.dev/specification/buyer-consent/) <br>
- [UCP specification overview](https://ucp.dev/specification/overview/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with implementation notes and code/configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no bundled executable code or hidden install behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
