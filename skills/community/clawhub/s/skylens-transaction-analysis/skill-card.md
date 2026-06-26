## Description: <br>
Inspects one EVM transaction with Skylens APIs and returns human-readable trace, balance, storage, and nonce changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certik-ai](https://clawhub.ai/user/certik-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and blockchain investigators use this skill to inspect a single supported EVM transaction, review call traces, check balance and storage changes, inspect nonce changes, and fetch related contract source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction hashes, chain names, and addresses are sent to CertiK Skylens during analysis. <br>
Mitigation: Use the skill only when sharing those transaction details with Skylens is acceptable for the user's investigation. <br>
Risk: The optional source-file output path can write fetched contract source to disk. <br>
Mitigation: Save source files only to an intended workspace path and avoid targeting sensitive or existing files. <br>


## Reference(s): <br>
- [CertiK Skylens](https://skylens.certik.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands] <br>
**Output Format:** [Plain text command output, with optional contract source content or a saved source-file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are scoped to one transaction and, where relevant, one holder, address, or source-file index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
