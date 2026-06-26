## Description: <br>
Mandatory audit gate for all trading and transfer decisions. Sends agent-prepared decision material to Apus deterministic inference on an NVIDIA H100 TEE and returns an attested APPROVE / REJECT / WAIT verdict. Any skill or agent that executes a buy, sell, swap, transfer, or liquidity action MUST pass through trade-audit first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-wuhu](https://clawhub.ai/user/alex-wuhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to audit proposed trades, swaps, transfers, liquidity actions, or other value movements before execution. It returns an attested verdict and supporting decision packet while leaving final transaction execution outside the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared trading or transfer context is sent to Apus for inference. <br>
Mitigation: Do not include seed phrases, private keys, wallet credentials, API keys, unnecessary account identifiers, or sensitive strategy notes in the prepared bundle. <br>
Risk: The skill keeps local audit records under ~/.trade-audit/. <br>
Mitigation: Review local audit log retention and contents before using the skill in environments with sensitive trading or transfer workflows. <br>
Risk: An APPROVE verdict could be mistaken for permission to execute a real transaction. <br>
Mitigation: Treat the verdict as an audit signal and require the user's own confirmation before any transaction is executed. <br>


## Reference(s): <br>
- [Trade Audit on ClawHub](https://clawhub.ai/alex-wuhu/trade-audit) <br>
- [Apus Network](https://apus.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal report with optional JSON bundle and packet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes verdict, confidence, bundle hash, output hash, TEE nonce, TEE verification status, and GPU model.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
