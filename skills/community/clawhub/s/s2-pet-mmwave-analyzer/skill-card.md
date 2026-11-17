## Description:

Transforms simulated mmWave radar signals into pet respiration metrics, fuses them with environmental context, and emits a diagnostic report plus a climate-control intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run a local pet-health signal-processing simulation, generate respiration analysis artifacts, and evaluate how environmental context could be routed into care recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill emits an automatic climate-control override intent from hardcoded simulated data.

Mitigation: Do not connect stdout to HVAC or other spatial controls unless explicit user approval, real sensor validation, and routing safeguards are added.

Risk: Runtime dependencies are specified with minimum versions rather than pinned hashes.

Mitigation: Install dependencies in an isolated environment and prefer pinned, hash-verified package versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-pet-mmwave-analyzer)
- [Publisher profile](https://clawhub.ai/user/spacesq)
- [Space2 homepage](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [Console text with a generated PNG diagnostic chart and installation commands in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an s2_pet_health_vault directory and writes pet_vital_radar_report.png when executed.]

## Skill Version(s):

1.1.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
