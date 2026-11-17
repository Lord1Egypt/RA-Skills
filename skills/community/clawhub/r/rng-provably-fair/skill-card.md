## Description:

Provably fair random number generation with on-chain seed anchoring for Keno, Roulette, and Dice entertainment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and verify random numbers for entertainment game flows where seed hashes, client seeds, revealed seeds, and Base-chain anchoring are part of the audit trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RNG requests are sent to the disclosed external sputnikx.xyz service.

Mitigation: Review and approve the external network dependency before use, and confirm the service's availability, terms, and expected data handling.

Risk: Casino-style claims such as house edge, RTP, and fairness can be misunderstood as financial advice or guarantees.

Mitigation: Treat those values as service claims, verify results through the documented proof process, and avoid presenting them as financial advice.

Risk: A proof trail only supports the specific seed, hash, result, and anchoring process it exposes.

Mitigation: Use the verification endpoint and disclosed seeds to audit individual results, and do not infer broader guarantees beyond the documented verification process.

## Reference(s):

- [SputnikX RNG documentation](https://sputnikx.xyz/rng/)
- [Generate random number API](https://sputnikx.xyz/rng/api/generate?min=1&max=100)
- [Verify result API](https://sputnikx.xyz/rng/api/verify/{seed_hash})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses disclosed external requests to sputnikx.xyz and does not require local environment variables.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
