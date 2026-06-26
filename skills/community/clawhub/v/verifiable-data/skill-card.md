## Description: <br>
Use Cryptowerk via curl to obtain service credentials, register hashes, fetch seals, and verify proofs for files or append-only records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[i001962](https://clawhub.ai/user/i001962) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Cryptowerk-backed proof workflows for verifiable logs, file-existence proofs, and deterministic local audit artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores sensitive Cryptowerk service credentials. <br>
Mitigation: Store issued apiKey/apiCredential tokens only in a private secret location, keep them out of committed or watched trees, and avoid logging them. <br>
Risk: The credential-issuance flow can involve an x402 paid retry. <br>
Mitigation: Do not allow an agent to complete any paid retry unless the user has explicitly approved the payment. <br>


## Reference(s): <br>
- [Cryptowerk API Notes](references/cryptowerk-api-notes.md) <br>
- [Storage and State](references/storage-and-state.md) <br>
- [ClawHub skill page](https://clawhub.ai/i001962/verifiable-data) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON sidecar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local retrieval id, seal, metadata, and verification response sidecar files for audited workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
