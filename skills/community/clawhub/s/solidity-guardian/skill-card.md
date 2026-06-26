## Description: <br>
Smart contract security analysis skill that detects vulnerabilities, suggests fixes, and generates audit reports for Hardhat and Foundry Solidity projects using pattern matching and Solidity security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to scan Solidity contracts or projects for common vulnerability patterns, review suggested fixes, and generate JSON or Markdown audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Slither wrapper can run shell commands from an unsafe project path. <br>
Mitigation: Run the Guardian-only analyzer or execute the skill in a sandbox until Slither invocation is changed to safe argument-based execution. <br>
Risk: The optional Slither installation path can install unpinned external tooling into the local Python environment. <br>
Mitigation: Avoid --install-slither unless intentional; install and pin Slither separately in a controlled environment. <br>
Risk: Automated smart contract findings and fix suggestions may be incomplete or misleading. <br>
Mitigation: Treat output as review support, validate findings manually, and obtain professional audit coverage for high-value contracts. <br>


## Reference(s): <br>
- [Solidity Security Best Practices](artifact/BEST_PRACTICES.md) <br>
- [Trail of Bits - Building Secure Contracts](https://github.com/crytic/building-secure-contracts) <br>
- [OpenZeppelin - Security Best Practices](https://docs.openzeppelin.com/learn/preparing-for-mainnet) <br>
- [Consensys - Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/) <br>
- [SWC Registry](https://swcregistry.io/) <br>
- [Slither](https://github.com/crytic/slither) <br>
- [Foundry Book - Security](https://book.getfoundry.sh/forge/security) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Console text, JSON, or Markdown audit reports with findings, severity, file locations, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally combine Guardian pattern findings with Slither findings and write reports to a file.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
