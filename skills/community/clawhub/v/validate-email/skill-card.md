## Description: <br>
Validate email addresses with format checking, disposable-domain detection, domain extraction, and local risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill to pre-filter signup, lead, or email-list inputs by checking email format, extracting domains, detecting known disposable providers, and returning a risk score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation includes Claw0x SDK and api.claw0x.com examples that may transmit email addresses to an external service despite local-handler privacy claims. <br>
Mitigation: Use the installed local handler for privacy-sensitive validation, and avoid the cloud API examples unless external transmission and CLAW0X_API_KEY handling are acceptable. <br>
Risk: The validator only checks syntax, built-in domain lists, and simple risk factors; it does not confirm that an address can receive mail. <br>
Mitigation: Do not treat a low risk score as proof of deliverability; use separate consented deliverability checks when that assurance is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennyzir/validate-email) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [Structured JSON object with validation status, normalized email, format and domain checks, risk score, and optional suggestion.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally in the installed handler; does not perform SMTP verification, DNS MX lookup, or deliverability checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
