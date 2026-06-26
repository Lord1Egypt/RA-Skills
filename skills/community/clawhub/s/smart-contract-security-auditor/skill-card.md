## Description: <br>
Smart Contract Security Auditor: Analyzes Solidity and Go smart contracts for security vulnerabilities, provides gas optimization suggestions, and generates corresponding test cases (Foundry or Go tests). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangter666](https://clawhub.ai/user/shangter666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart contract engineers use this skill to review Solidity and Go contract code for common vulnerabilities, identify gas or state-access optimizations, and generate Foundry or Go test cases. It is intended as a review aid whose findings and generated tests should be manually verified before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit findings, optimization suggestions, or generated tests may be incomplete or incorrect for a specific contract, framework, or deployment context. <br>
Mitigation: Manually verify all findings, optimizations, and tests before applying changes to production or deployed contracts. <br>
Risk: Generated Foundry or Go tests may not cover project-specific invariants, authorization models, or chain-specific behavior. <br>
Mitigation: Run the project's existing test suite and have qualified smart contract reviewers extend generated tests for critical logic before merge or deployment. <br>


## Reference(s): <br>
- [Common Smart Contract Vulnerabilities](references/vulnerabilities.md) <br>
- [Gas and Performance Optimization](references/gas_optimization.md) <br>
- [Testing Strategies](references/testing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shangter666/smart-contract-security-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with audit findings, optimization recommendations, and Solidity or Go test code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Foundry test snippets, Go testing package examples, and manual review guidance for production or deployed contracts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
