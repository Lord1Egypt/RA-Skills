## Description: <br>
Implement UCP AP2 Mandates for cryptographic payment authorization in autonomous agent commerce using SD-JWT credentials, merchant authorization signatures, and the Agent Payments Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichiorca](https://clawhub.ai/user/ichiorca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building UCP/AP2 autonomous checkout flows use this skill for guidance on mandate artifacts, merchant authorization signatures, verification flow, and AP2-specific error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill supports autonomous payment flows and is associated with crypto and purchase capabilities, so misuse or overbroad credentials could enable unintended spending. <br>
Mitigation: Install only for agents that are intentionally allowed to spend from a dedicated, limited wallet; enforce external spending limits and recipient or network restrictions, fund only acceptable loss amounts, monitor transaction history, and rotate wallet secrets if exposure is suspected. <br>


## Reference(s): <br>
- [UCP and AP2 documentation](https://ucp.dev/2026-01-23/documentation/ucp-and-ap2/) <br>
- [Agent Payments Protocol](https://ap2-protocol.org) <br>
- [Universal Commerce Protocol conformance suite](https://github.com/Universal-Commerce-Protocol/conformance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown guidance with implementation notes and protocol references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to fetch current external protocol specifications before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
