## Description: <br>
Autonomous yield farming agent for BNB Chain with deterministic execution, smart contract integration, and automated decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alannetwork](https://clawhub.ai/user/alannetwork) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to evaluate BNB Chain vault data, produce deterministic yield-farming decisions, and optionally execute or schedule blockchain actions with audit hashes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous transaction execution can sign and broadcast blockchain actions with a raw private key. <br>
Mitigation: Use testnet or local evaluation by default; require hardware-wallet or KMS signing, explicit transaction limits, and human approval before mainnet use. <br>
Risk: The release includes testnet and stub contract code with mixed production-readiness messaging. <br>
Mitigation: Do not use the bundled stub YieldVault contract in production; require audited contracts and a mainnet readiness review before deploying with real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alannetwork/yieldvault-agent) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [User guide](artifact/README.md) <br>
- [Live execution guide](artifact/LIVE_EXECUTION_GUIDE.md) <br>
- [Production readiness checklist](artifact/FINAL_CHECKLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON execution records, JavaScript code, and Markdown documentation with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution records include deterministic decision and execution hashes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
