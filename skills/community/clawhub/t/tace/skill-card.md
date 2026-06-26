## Description: <br>
TACE (Tender Agentic Commerce Engine) runtime contract that provides concrete endpoint payloads and response schemas for authenticated commerce workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tender](https://clawhub.ai/user/tender) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to integrate agents with TACE commerce APIs for authentication, product discovery, ordering, payment status updates, subscriptions, waitlists, and feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables wallet-backed purchases and account or order changes. <br>
Mitigation: Require explicit user approval before wallet signing, registration, order placement, cancellation, payment-status changes, agent deactivation, feedback submission, or webhook and subscription setup. <br>
Risk: The skill may require sensitive wallet-related credentials or signing material. <br>
Mitigation: Do not provide private keys or seed phrases, and redact sensitive values in outputs, traces, and logs. <br>


## Reference(s): <br>
- [TACE skill page](https://clawhub.ai/tender/tace) <br>
- [TACE homepage](https://tender.cash) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; optional TACE_ENV and TACE_SKILL_VERSION environment variables are documented.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
