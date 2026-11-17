## Description:

Upload and download files to and from the Stratos Decentralized Storage (SDS) network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notboxqsn](https://clawhub.ai/user/notboxqsn)

### License/Terms of Use:


## Use Case:

External users, developers, and engineers use this skill to upload local files to Stratos SDS, retrieve files by hash or CID, and configure a local Stratos resource node when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to a decentralized storage network.

Mitigation: Use it only for explicit upload requests, confirm the file path with the user, and avoid uploading sensitive files.

Risk: Downloads retrieve network content and write it to a local destination.

Mitigation: Choose a private trusted destination directory, avoid overwriting existing files, and review downloaded content before use.

Risk: Node setup can involve wallet mnemonics, passwords, staking amounts, and fees.

Mitigation: Keep wallet secrets outside chats and source-controlled files, and verify the network, wallet, amount, and fees before staking STOS.

Risk: Running a Stratos node may expose service ports.

Mitigation: Restrict node service ports with a firewall and expose only the interfaces required for the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/notboxqsn/skills/stratos-storage)
- [Stratos SDS Resource Node Setup Guide](artifact/docs/setup-guide-en.md)
- [Stratos SDS Resource Node Setup Guide (Chinese)](artifact/docs/setup-guide-zh.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown status text with inline shell commands, file paths, and file identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return CIDs, output paths, upload/download status, and Stratos node setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
