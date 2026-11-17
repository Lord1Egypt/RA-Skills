## Description:

Solidity Guardian analyzes Solidity smart contracts to detect vulnerabilities, suggest fixes, and generate audit-style reports for Hardhat and Foundry projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to scan Solidity contracts, review vulnerability findings, and produce remediation guidance before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Slither wrapper can run unsafe shell commands from a crafted project path.

Mitigation: Use only trusted local paths, avoid untrusted or generated path strings, and run the skill in an isolated environment until command construction is fixed.

Risk: The optional Slither installer can install unpinned tools.

Mitigation: Preinstall a pinned Slither version in an isolated environment instead of using --install-slither.

Risk: Running the skill with broad privileges can increase impact if command execution is exploited.

Mitigation: Do not run it as root or in CI jobs with broad secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aviclaw/skills/solidity-guardian)
- [Trail of Bits - Building Secure Contracts](https://github.com/crytic/building-secure-contracts)
- [OpenZeppelin - Security Best Practices](https://docs.openzeppelin.com/learn/preparing-for-mainnet)
- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [SWC Registry](https://swcregistry.io/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Slither](https://github.com/crytic/slither)
- [Foundry Book - Security](https://book.getfoundry.sh/forge/security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JSON or Markdown audit findings with severity, location, description, recommendation, and references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write audit reports to a user-selected output file.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter and package.json show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
