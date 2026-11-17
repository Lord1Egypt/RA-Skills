## Description:

Trade Audit prepares and submits trading or transfer decision material to Apus deterministic inference and returns an attested approve, reject, or wait verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-wuhu](https://clawhub.ai/user/alex-wuhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a pre-execution review for buy, sell, swap, transfer, liquidity, or other value-movement decisions. It helps organize relevant facts, call an external audit service, and return a verdict with attestation fields and optional saved audit artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prepared financial decision material is sent to Apus and audit details are stored in a local log.

Mitigation: Use only when users are comfortable sharing the prepared material with Apus, avoid including unnecessary sensitive details, and protect or review the local audit log.

Risk: The security review says the skill tries to become a mandatory gate for trades and transfers with weak controls.

Mitigation: Do not rely on it as the sole approval mechanism for irreversible trades or transfers; require separate user confirmation, deterministic local limits, and independent attestation verification.

## Reference(s):

- [Apus Network](https://apus.network)
- [Apus deterministic inference endpoint](https://hb.apus.network/~inference@1.0)
- [Trade Audit ClawHub page](https://clawhub.ai/alex-wuhu/skills/trade-audit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown preparation templates, and JSON audit artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write normalized bundle and packet files, append a local audit log, and use gate-mode exit codes for approve, reject, or wait verdicts.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
