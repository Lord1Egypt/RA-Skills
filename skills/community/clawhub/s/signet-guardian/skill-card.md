## Description: <br>
Payment guard middleware for AI agents that checks payment requests against user policy and records successful payments through Signet commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafalzacher1](https://clawhub.ai/user/rafalzacher1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators of payment-capable AI agent skills use Signet Guardian to preflight payment attempts, enforce configured limits, request confirmation when policy requires it, and record completed payments for audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled fallback policy enables small payments before the user has necessarily opted in. <br>
Mitigation: Review and replace the bundled policy before connecting payment-capable skills, and set paymentsEnabled to false until the user intentionally opts in. <br>
Risk: Payment-capable skills could bypass protection if they do not honor Signet Guardian decisions. <br>
Mitigation: Confirm integrating skills always call signet-preflight, respect DENY and CONFIRM_REQUIRED, and call signet-record after successful payments. <br>
Risk: The local ledger may contain sensitive payment history. <br>
Mitigation: Keep the ledger private and restrict policy editing or migration commands to trusted, user-directed sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rafalzacher1/signet-guardian) <br>
- [Signet Homepage](https://getsignet.xyz) <br>
- [Skill Contract](SKILL.md) <br>
- [README](README.md) <br>
- [OpenClaw Extension README](openclaw-extension/README.md) <br>
- [Default Policy Reference](references/policy.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command results and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preflight returns ALLOW, DENY, or CONFIRM_REQUIRED; record and report commands update or summarize the local payment ledger.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
