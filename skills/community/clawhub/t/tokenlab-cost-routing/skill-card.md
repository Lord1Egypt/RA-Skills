## Description:

Choose TokenLab models and fallback chains using public pricing, task fit, latency expectations, and native endpoint needs before writing production routing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hedging8563](https://clawhub.ai/user/hedging8563)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compare public TokenLab model pricing and capabilities, then design cost-aware routes and fallbacks for their workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog or pricing changes can make cost estimates and fallback choices stale.

Mitigation: Check live public catalog and pricing before recommending routes; state units and assumptions, and disclose when prices cannot be verified.

Risk: Switching to a cheaper model can change capabilities, structured outputs, safety behavior, or incur unexpected paid-media costs.

Mitigation: Check endpoint and capability requirements before switching, and require user approval before automatic paid-media fallbacks or quality reductions.

Risk: Installation or lookup queries may expose sensitive workload details or depend on an unpinned installer source.

Mitigation: Verify or pin the installer source where reproducibility matters; keep lookup queries limited to non-sensitive workload categories, model IDs, and pricing assumptions.

## Reference(s):

- [TokenLab Cost Routing on ClawHub](https://clawhub.ai/hedging8563/skills/tokenlab-cost-routing)
- [TokenLab model catalog](https://api.tokenlab.sh/v1/models)
- [TokenLab model pricing endpoint](https://api.tokenlab.sh/v1/models/{model}/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown routing table with catalog and pricing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workload assumptions, endpoint choices, fallback conditions, and cost caveats.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
