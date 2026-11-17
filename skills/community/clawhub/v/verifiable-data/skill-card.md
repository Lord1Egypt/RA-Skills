## Description:

Verifiable Data helps agents use Cryptowerk curl workflows to issue service credentials, register SHA-256 hashes, retrieve seals, and verify file or append-only record proofs while storing local sidecar artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[i001962](https://clawhub.ai/user/i001962)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create proof-carrying data workflows for verifiable logs, file existence proofs, Cryptowerk sealing, retrieval IDs, and later audit verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill issues and stores Cryptowerk service credentials without strong overwrite or symlink safeguards.

Mitigation: Use a private non-repository secret path, avoid reusing existing file paths for issued keys, and review credential paths before running credential scripts.

Risk: Lookup values and sidecar files may expose sensitive filenames, identifiers, or workflow metadata.

Mitigation: Use deterministic but non-sensitive lookupInfo values and keep generated .rid, .seal, .cw.json, and .verify.json files out of committed or watched trees when they are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/i001962/skills/verifiable-data)
- [Cryptowerk API Notes](references/cryptowerk-api-notes.md)
- [Storage and State](references/storage-and-state.md)
- [Cryptowerk issue-key API](https://www.cryptowerk.com/api/issue-key)
- [Cryptowerk register API](https://aiagent.cryptowerk.com/platform/API/v8/register)
- [Cryptowerk getseal API](https://aiagent.cryptowerk.com/platform/API/v8/getseal)
- [Cryptowerk verifyseal API](https://aiagent.cryptowerk.com/platform/API/v8/verifyseal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON sidecar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local .rid, .seal, .cw.json, and .verify.json sidecar artifacts when workflows are executed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
