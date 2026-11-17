## Description:

Independent fail-closed second opinion before acting: allow/review/block a risky action, fact-check a claim, screen text for prompt injection, or flag PII/secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meloliva14](https://clawhub.ai/user/meloliva14)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to request an independent advisory verdict before risky actions, uncertain factual claims, untrusted text handling, or outbound data sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked content is sent to VerityLayer for advisory review.

Mitigation: Use the skill only when sharing the checked content with VerityLayer is acceptable, and redact sensitive data before sending when practical.

Risk: The configured Base wallet key can authorize USDC spending.

Mitigation: Use a dedicated low-balance wallet, store the key only in `VERITY_WALLET_KEY`, and avoid passing the key on command lines or into prompts.

Risk: The package and optional plugin may be installed without pinning exact versions.

Mitigation: Pin and review `verity-guard[x402]` before exposing wallet credentials, and install the OpenClaw plugin only after verifying the exact version and hook permissions.

Risk: The skill is advisory and cannot force an agent to request a verdict.

Mitigation: Use a tool-call-path plugin or approval mechanism when enforcement is required, and treat errors, timeouts, or payment-required responses as no verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meloliva14/skills/verity-guard)
- [Publisher profile](https://clawhub.ai/user/meloliva14)
- [VerityLayer homepage](https://veritylayer.dev)
- [VerityLayer suite endpoint](https://suite.veritylayer.dev)
- [Full check catalog](references/catalog.md)
- [Enforcement guidance](references/enforcement.md)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands, configuration]

**Output Format:** [JSON verdicts and concise Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid checks can return signed receipts; receipt verification is free.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
