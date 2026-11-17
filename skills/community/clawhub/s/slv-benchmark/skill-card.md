## Description:

Run benchmark tests and connectivity checks for SLV endpoints using shredstream, grpc, or rpc with region-aware configuration and API key support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poppin-fumi](https://clawhub.ai/user/poppin-fumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to compare Solana shredstream, gRPC, and RPC endpoint behavior, generate benchmark configuration, and run local connectivity checks with region-aware inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark setup may read an existing local SLV ERPC API key file and generated configuration or logs may expose that key if shared.

Mitigation: Avoid sharing generated configuration or logs unless secrets are redacted, and prefer environment-based or otherwise protected secret handling when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poppin-fumi/skills/slv-benchmark)
- [SLV project repository](https://github.com/ValidatorsDAO/slv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct benchmark output when local tools are available.]

## Skill Version(s):

0.13.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
