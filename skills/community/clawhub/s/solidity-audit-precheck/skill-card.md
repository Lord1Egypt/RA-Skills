## Description: <br>
Automated pre-audit checklist for Solidity smart contracts that runs SWC registry checks, OpenZeppelin pattern validation, gas optimization review, and common vulnerability detection before manual audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart contract security reviewers use this skill to run a Solidity pre-audit workflow before paid manual audits, major releases, or mainnet/testnet deployment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to install and run third-party Solidity analysis tools locally. <br>
Mitigation: Use a virtual environment or container, verify tool sources before installation, and run the skill only in Solidity repositories intended for analysis. <br>
Risk: Automated Solidity scanners can miss business logic, economic invariant, access control, and oracle risks. <br>
Mitigation: Treat the output as a pre-audit filter and require manual review before deployment or paid audit handoff. <br>
Risk: Generated reports may contain sensitive source details or vulnerability findings. <br>
Mitigation: Review reports before sharing them outside the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/solidity-audit-precheck) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>
- [SWC Registry](https://swcregistry.io/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with checklist items, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analysis workflow guidance and a pre-audit report template; it does not replace manual audit judgment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
