## Description: <br>
Solidity Audit is a smart contract security audit assistant that follows the EEA EthTrust V3 specification and supports structured vulnerability scanning, manual security analysis, audit reporting, Slither/Aderyn static analysis, and Foundry testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaominger](https://clawhub.ai/user/xiaominger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and auditors use this skill to structure Solidity and EVM smart contract audits, map findings to EEA EthTrust levels, run or interpret static-analysis and testing workflows, and produce audit report drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-generated audit reports may miss business-logic, math-boundary, or complex-interaction issues in high-value contracts. <br>
Mitigation: Use the skill output as structured audit assistance and require professional human review, static analysis, fuzz testing, and project-specific verification before relying on findings. <br>
Risk: The workflow includes optional package installation and curl-to-bash setup commands for external audit tools. <br>
Mitigation: Verify tool sources and versions before execution, and run setup commands only in a controlled development workspace. <br>
Risk: Automated scanners can produce false positives or miss context-specific Solidity vulnerabilities. <br>
Mitigation: Correlate scanner output with manual review, protocol-specific templates, test results, and EEA EthTrust requirement mapping. <br>


## Reference(s): <br>
- [Audit Methodology](references/audit-methodology.md) <br>
- [EEA EthTrust Security Levels V3 Specification Guide](references/eea-requirements.md) <br>
- [Audit Report Template](references/report-template.md) <br>
- [SecureUM Mind Map Knowledge Base](references/secureum-knowledge.md) <br>
- [Solidity Testing Guide](references/testing-guide.md) <br>
- [Audit Toolchain Configuration Guide](references/toolchain-guide.md) <br>
- [Solidity Vulnerability Checklist](references/vulnerability-checklist.md) <br>
- [Cross-Chain Protocol Audit Template](references/protocol-templates/cross-chain.md) <br>
- [DEX Aggregator Protocol Audit Template](references/protocol-templates/dex-aggregator.md) <br>
- [EEA EthTrust Security Levels V3](https://entethalliance.org/specs/ethtrust-sl/v3/) <br>
- [Slither](https://github.com/crytic/slither) <br>
- [Aderyn](https://github.com/Cyfrin/aderyn) <br>
- [Foundry](https://github.com/foundry-rs/foundry) <br>
- [Echidna](https://github.com/crytic/echidna) <br>
- [Mythril](https://github.com/ConsenSys/mythril) <br>
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts) <br>
- [Ethereum Improvement Proposals](https://eips.ethereum.org/all) <br>
- [Mastering Ethereum](https://masteringethereum.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Solidity snippets, JSON findings templates, and audit report outlines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate an audit workspace scaffold and draft findings/report artifacts when the included initialization script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
