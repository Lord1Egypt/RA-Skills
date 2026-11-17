## Description:

Secure Storage provides AES-based local storage commands for saving and retrieving API keys and other sensitive values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for low-risk local convenience when setting, retrieving, listing, and deleting locally stored key-value secrets. It should not be used for production credential protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored secrets can be exposed if users rely on this version for real credential protection.

Mitigation: Use only for low-risk local convenience; do not store production API keys, cloud credentials, repository tokens, or account secrets.

Risk: The local storage approach does not provide the protections expected from a credential manager.

Mitigation: Prefer an OS keychain, password manager, KMS-backed secret store, or a revised version using user-controlled key material and authenticated encryption.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CLI text output with local JSON storage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries in a local file under the user's home directory.]

## Skill Version(s):

1.0.1 (source: frontmatter, skill.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
