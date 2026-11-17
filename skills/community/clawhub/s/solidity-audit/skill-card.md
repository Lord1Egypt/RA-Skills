## Description:

Solidity Audit helps agents perform structured Solidity smart contract security reviews using EEA EthTrust V3 guidance, vulnerability checklists, Slither and Aderyn static analysis, Foundry testing, and audit report templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaominger](https://clawhub.ai/user/xiaominger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, and security engineers use this skill to plan and conduct smart contract reviews, map findings to EEA EthTrust security levels, interpret static-analysis and test results, and prepare audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the skill documents unsafe curl-to-bash installer commands for Foundry.

Mitigation: Review installation steps before use and prefer pinned releases, checksums or signatures, locked package-manager installs, or an isolated container.

Risk: The audit project helper script can write outside the chosen folder if given project names containing path traversal or separators.

Mitigation: Use simple project names without slashes or dot-dot components until path validation is added, and review generated paths before running the script.

Risk: AI-assisted audit guidance can miss business-logic, math-boundary, and complex-interaction vulnerabilities.

Mitigation: Use this skill as support for human security review, run the recommended analysis and testing tools, and independently validate findings before relying on a report.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xiaominger/skills/solidity-audit)
- [EEA EthTrust Security Levels V3](https://entethalliance.org/specs/ethtrust-sl/v3/)
- [SecureUM Mind Map](https://github.com/x676f64/secureum-mind_map)
- [Slither](https://github.com/crytic/slither)
- [Aderyn](https://github.com/Cyfrin/aderyn)
- [Foundry](https://github.com/foundry-rs/foundry)
- [Echidna](https://github.com/crytic/echidna)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Ethereum Improvement Proposals](https://eips.ethereum.org/all)
- [Mastering Ethereum](https://masteringethereum.xyz/)
- [Smart Contract Audit Methodology](artifact/references/audit-methodology.md)
- [Audit Report Template](artifact/references/report-template.md)
- [Solidity Vulnerability Checklist](artifact/references/vulnerability-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Solidity, JSON, YAML, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide audit workflows and may scaffold audit project files when an agent runs the helper script.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
