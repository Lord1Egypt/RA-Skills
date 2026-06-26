## Description: <br>
Verify and inspect smart contracts on the QELT blockchain using the Mainnet Indexer verification API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PRQELT](https://clawhub.ai/user/PRQELT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check QELT contract verification status, submit single-file or multi-file Solidity verification jobs, retrieve ABIs and source code, and inspect supported compiler or EVM versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted Solidity source, constructor arguments, and library details may become public after successful verification. <br>
Mitigation: Review the exact files and values before submission, and do not submit private keys, secrets, proprietary code that should remain private, or unreviewed local files. <br>
Risk: Repeated submissions can consume the QELT verification rate limit or duplicate a job already in progress. <br>
Mitigation: Check existing verification status before submitting, poll active jobs instead of re-submitting, and follow Retry-After guidance after HTTP 429 responses. <br>
Risk: Optional Hardhat plugin and CLI tooling introduce separate package dependencies. <br>
Mitigation: Review those npm packages independently before installing or using them. <br>


## Reference(s): <br>
- [QELT Contract Verification Reference Guide](references/verification-guide.md) <br>
- [QELT Mainnet Indexer](https://mnindexer.qelt.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/PRQELT/qelt-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl against QELT verification endpoints; verification submissions are rate limited to 10 per hour per IP.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
