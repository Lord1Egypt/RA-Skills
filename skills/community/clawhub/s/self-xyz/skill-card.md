## Description: <br>
Integrate Self (self.xyz), a privacy-first identity protocol, to verify passports and ID cards with zero-knowledge proofs across frontend QR code, backend API, and Celo smart contract flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xturboblitz](https://clawhub.ai/user/0xturboblitz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add privacy-preserving KYC, age verification, nationality checks, OFAC screening, or Sybil-resistance flows based on Self identity proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Identity verification flows can expose sensitive passport or ID attributes if applications request, log, retain, or disclose raw personal data unnecessarily. <br>
Mitigation: Prefer predicate checks such as minimum age or sanctions status, avoid passport or ID numbers unless legally required, and define deletion, retention, and access controls before production use. <br>
Risk: On-chain integrations can permanently expose personal data if raw identity fields are emitted or stored by smart contracts. <br>
Mitigation: Do not store or emit raw personal data on-chain; use proof outcomes, nullifiers, or minimal status flags instead. <br>
Risk: Development settings for mock passports or staging networks can weaken production verification if left enabled. <br>
Mitigation: Disable mock-passport and staging settings in production and verify that frontend disclosures exactly match backend or contract verification configuration. <br>


## Reference(s): <br>
- [Backend Integration](references/backend.md) <br>
- [Smart Contract Integration](references/contracts.md) <br>
- [Frontend Integration](references/frontend.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, Solidity, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes integration patterns, configuration notes, deployed Celo contract addresses, and privacy guardrails.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
