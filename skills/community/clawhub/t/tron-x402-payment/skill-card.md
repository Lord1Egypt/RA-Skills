## Description:

Pay for x402-enabled Agent endpoints using TRC20 tokens (USDT/USDD) on TRON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzc1206](https://clawhub.ai/user/wzc1206)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to invoke x402-enabled agent endpoints and automatically handle TRON TRC20 payments for USDT or USDD when a 402 payment response is returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a TRON private key to authorize payments and may grant broad token allowances.

Mitigation: Use a dedicated low-balance wallet, prefer trusted HTTPS endpoints, and revoke token allowances after use.

Risk: Credential lookup can include environment variables and local configuration files, including mcporter credentials.

Mitigation: Use the built-in status check instead of printing environment variables, and avoid relying on unrelated credential stores.

Risk: Binary endpoint responses may be saved as temporary files.

Mitigation: Delete temporary files after they are inspected or passed to the next workflow step.

## Reference(s):

- [x402](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/wzc1206/skills/tron-x402-payment)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Endpoint response as text or JSON; binary responses are saved to temporary files with JSON metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May authorize TRC20 token payments, grant token allowance, retry the endpoint with an X-PAYMENT header, and require cleanup of temporary output files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter 1.1.0 and package.json 1.0.1 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
