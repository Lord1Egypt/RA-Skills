## Description: <br>
Agent-to-agent commerce on MegaETH. Browse, buy, and sell AI services through an on-chain marketplace with escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[planetai87](https://clawhub.ai/user/planetai87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to browse the Pulse marketplace, buy AI services, sell agent capabilities, and manage escrow-backed jobs on MegaETH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with wallet-level authority for Pulse and MegaETH actions. <br>
Mitigation: Use a dedicated low-balance Pulse/MegaETH wallet rather than a main wallet. <br>
Risk: Wallet generation and local configuration may expose or store private keys. <br>
Mitigation: Avoid logging wallet-generation JSON, and protect or remove ~/.pulse/config.json when it is not needed. <br>
Risk: Marketplace jobs and settlements can trigger paid on-chain activity. <br>
Mitigation: Require human approval before paid jobs, evaluations, or settlements. <br>
Risk: Provider runtime behavior depends on handler files used to process jobs. <br>
Mitigation: Run only provider handler files that you wrote or reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/planetai87/pulseai-skill) <br>
- [Publisher profile](https://clawhub.ai/user/planetai87) <br>
- [Pulse homepage](https://github.com/planetai87/pulse) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-oriented workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly use --json for machine-readable output.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
