## Description: <br>
Provision a dedicated inbox for your AI agent and manage email safely via thrd.email. Includes instant onboarding, inbound polling, reply/send (idempotent + policy-gated), Proof of Reasoning for cold outbound, Human Claiming for verification, and trust/delivery tracking. Does not persist API keys to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SergioRico1](https://clawhub.ai/user/SergioRico1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to provision and operate a dedicated thrd.email inbox for an AI agent, including onboarding, inbound polling, replies, sends, delivery tracking, billing upgrades, and human verification flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a dedicated email inbox and initiate outbound email or billing-related flows. <br>
Mitigation: Define clear human approval rules for outbound email, billing upgrades, and verification flows before deployment. <br>
Risk: THRD_API_KEY grants access to authenticated thrd.email operations. <br>
Mitigation: Store THRD_API_KEY in a secret manager or runtime environment and do not write it to disk. <br>
Risk: The optional poll-daemon callback can run local commands when events arrive. <br>
Mitigation: Use only harmless callback commands that the operator would run directly; shell operators are unsupported and callbacks run without a shell. <br>
Risk: Using a non-default API endpoint can route email operations through an untrusted service. <br>
Mitigation: Use the default Thrd API endpoint unless the alternative endpoint is trusted. <br>


## Reference(s): <br>
- [Thrd API Reference](references/api.md) <br>
- [Thrd Skill on ClawHub](https://clawhub.ai/SergioRico1/thrd-skill) <br>
- [Thrd Email](https://thrd.email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3, the requests package, and THRD_API_KEY for authenticated API operations.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
