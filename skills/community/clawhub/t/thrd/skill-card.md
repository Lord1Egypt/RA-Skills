## Description: <br>
Provision a dedicated inbox for your AI agent and manage email safely via thrd.email. Includes instant onboarding, inbound polling, reply/send (idempotent + policy-gated), Proof of Reasoning for cold outbound, Human Claiming for verification, and trust/delivery tracking. Does not persist API keys to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SergioRico1](https://clawhub.ai/user/SergioRico1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to provision a dedicated Thrd email inbox, poll inbound events, send or reply to email with policy gates, and route billing or verification steps to a responsible human. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates an email inbox and can perform outbound email actions. <br>
Mitigation: Require human approval for outbound email workflows and follow the skill's policy-gated send, reply, Proof of Reasoning, and Prompt Shield acknowledgement steps. <br>
Risk: THRD_API_KEY grants access to the Thrd inbox tools if exposed. <br>
Mitigation: Store THRD_API_KEY in a secret manager, avoid writing it to disk, and reveal onboarding keys only in a trusted terminal. <br>
Risk: Billing checkout and verification flows can affect account state or payment setup. <br>
Mitigation: Forward Stripe checkout and human-claiming URLs to the responsible human owner instead of completing those flows autonomously. <br>
Risk: Long-running polling can continue processing inbound events without continuous supervision. <br>
Mitigation: Supervise the polling daemon, prefer signed wake webhooks when available, and review cursor-file behavior before deployment. <br>


## Reference(s): <br>
- [Thrd API Reference](references/api.md) <br>
- [Thrd Email](https://thrd.email) <br>
- [ClawHub Skill Page](https://clawhub.ai/SergioRico1/thrd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and THRD_API_KEY for authenticated tools; onboarding redacts API keys unless explicitly requested.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
