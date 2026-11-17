## Description:

Smart Contract Security Auditor: Analyzes Solidity and Go smart contracts for security vulnerabilities, provides gas optimization suggestions, and generates corresponding test cases (Foundry or Go tests).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangter666](https://clawhub.ai/user/shangter666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit Solidity and Go smart contracts, identify common vulnerabilities, suggest gas or performance improvements, and draft Foundry or Go tests for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit findings or tests may be incomplete or incorrect for contracts that control funds or production chain state.

Mitigation: Review findings and generated test changes before applying them, and run project-specific security checks and test suites.

Risk: Optimization suggestions may change contract behavior, gas use, or state access patterns if applied without validation.

Mitigation: Apply suggested changes in a controlled branch and validate behavior with Foundry, Go tests, and manual review before deployment.

## Reference(s):

- [Common Smart Contract Vulnerabilities](references/vulnerabilities.md)
- [Gas and Performance Optimization](references/gas_optimization.md)
- [Testing Strategies](references/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses with audit findings, optimization suggestions, and Solidity or Go test code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Foundry or Go test files for user review; no hidden execution or persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
