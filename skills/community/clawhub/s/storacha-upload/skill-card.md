## Description:

Upload, manage, and retrieve files on IPFS through Storacha decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adielliot37](https://clawhub.ai/user/adielliot37)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent set up Storacha CLI access, upload files or directories to IPFS, manage spaces and delegations, retrieve gateway links, remove uploads, and report account storage usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files uploaded to Storacha/IPFS are public to anyone with the CID or gateway URL.

Mitigation: Confirm each upload and encrypt secrets or sensitive personal files before upload.

Risk: Removing an upload from a Storacha listing may not erase copies retained elsewhere on IPFS.

Mitigation: Treat uploads as permanent and warn users before deletion-sensitive workflows.

Risk: The skill can direct uploads, deletions, space switches, and delegations for a user's Storacha account.

Mitigation: Require explicit user confirmation for uploads, deletions, space changes, and delegations, and avoid full-admin delegations unless the recipient is fully trusted.

Risk: Global CLI installation can introduce supply-chain exposure if the Storacha CLI source is not reviewed.

Mitigation: Use a pinned, reviewed Storacha CLI installation and verify Node.js v18 or higher before use.

## Reference(s):

- [Storacha Documentation](https://docs.storacha.network)
- [Storacha Console](https://console.storacha.network)
- [Storacha CLI Reference](https://github.com/storacha/storacha/tree/main/packages/cli)
- [IPFS Gateway](https://storacha.link)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and human-readable status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Storacha gateway URLs, CIDs, storage usage summaries, account setup guidance, and delegation files when requested.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
