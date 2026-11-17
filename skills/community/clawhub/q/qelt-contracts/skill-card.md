## Description:

Verify, inspect, and retrieve verified Solidity smart contracts, ABIs, and compiler/EVM versions on the QELT blockchain using the Mainnet Indexer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prqelt](https://clawhub.ai/user/prqelt)

### License/Terms of Use:


## Use Case:

Developers and smart contract maintainers use this skill to verify Solidity contracts on QELT, retrieve verified source code or ABI data, and choose matching compiler and EVM settings before submitting verification jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional npm or global tooling may run mutable third-party code when package versions are not pinned.

Mitigation: Prefer the direct curl/API workflow where possible; before using the optional Hardhat plugin or CLI, pin exact package versions, avoid global installs, and review npm package provenance and lifecycle scripts.

Risk: Submitted contract source code becomes public if verification succeeds.

Mitigation: Inspect source files before submission, remove private keys or secrets, and confirm that public disclosure is intended.

## Reference(s):

- [QELT Mainnet Indexer](https://mnindexer.qelt.ai)
- [QELT Contract Verification Reference Guide](references/verification-guide.md)
- [ClawHub skill page](https://clawhub.ai/prqelt/skills/qelt-contracts)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API responses, ABI or source retrieval guidance, and status polling instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
