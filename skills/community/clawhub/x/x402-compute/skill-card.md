## Description:

Helps agents provision and manage compute, use the SGL Grid, deploy hosted agent pods and paid processors, and run training, dataset generation, and encrypted agent backups through Singularity Cloud Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivaavimusic](https://clawhub.ai/user/ivaavimusic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform operators use this skill to manage GPU and VPS instances, access inference and media APIs, deploy hosted agents and paid processors, and run dataset, training, and backup workflows through Singularity Cloud Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious, citing risky installation guidance, credential-handling concerns, and gaps in safeguards; some referenced material was only partially analyzed.

Mitigation: Consider avoiding installation until you verify the installer and package versions, understand credential and data handling, and confirm safeguards for destructive actions.

Risk: Payment workflows use private keys to sign blockchain transactions.

Mitigation: Use a dedicated wallet with limited funds and keep signing secrets private, as the skill's security notice advises.

## Reference(s):

- [x402 Compute documentation](https://docs.x402layer.cc/agentic-access/x402-compute)
- [Singularity Cloud dashboard](https://cloud.x402compute.cc)
- [API Reference](artifact/references/api-reference.md)
- [Agent Pods API](artifact/references/agent-pods-api.md)
- [SGL Processors](artifact/references/processors.md)
- [Datasets](artifact/references/datasets.md)
- [Training Lab](artifact/references/training.md)
- [Agent Vault](artifact/references/agent-vault.md)
- [Grid transcription](artifact/references/transcription.md)
- [Multimodal embeddings](artifact/references/multimodal-embeddings.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API requests, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, JSON/HTTP examples, and service-generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows can trigger paid compute, blockchain payments, data processing, or instance lifecycle actions.]

## Skill Version(s):

1.36.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
