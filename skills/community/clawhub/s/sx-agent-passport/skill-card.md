## Description: <br>
Issue and verify SX# agent passports with cryptographic identity, hash-chain integrity, and Merkle anchoring on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register AI agents, retrieve SX# passports, inspect agent profiles, and verify event or Merkle proofs through the disclosed Soul service API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples contact an external service and submit agent registration information. <br>
Mitigation: Only submit agent information intended for registration with the disclosed Soul service. <br>
Risk: The registration example can request and return an API key. <br>
Mitigation: Keep returned API keys private and avoid sharing them in prompts, logs, or public artifacts. <br>
Risk: Some verification endpoints are labeled as paid. <br>
Mitigation: Confirm cost and authorization before calling paid proof or Merkle verification endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drivenbymyai-max/sx-agent-passport) <br>
- [SoulLedger Homepage](https://soulledger.sputnikx.xyz) <br>
- [Soul API Base](https://soul.sputnikx.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples contact an external service and may return an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
