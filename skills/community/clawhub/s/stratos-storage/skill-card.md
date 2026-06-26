## Description: <br>
Upload and download files to/from Stratos Decentralized Storage (SDS) network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notboxqsn](https://clawhub.ai/user/notboxqsn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to upload files to Stratos SDS, retrieve files by hash or CID, and receive setup guidance for a Stratos resource node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploading the wrong file can send unintended content to the configured Stratos storage gateway. <br>
Mitigation: Confirm exact file paths before upload and avoid uploading sensitive files accidentally. <br>
Risk: A misconfigured or untrusted STRATOS_SPFS_GATEWAY can send upload and download traffic to the wrong node. <br>
Mitigation: Verify STRATOS_SPFS_GATEWAY points to a trusted Stratos SDS node before running upload or download commands. <br>
Risk: Resource node setup involves wallet mnemonics, passwords, staking, and node startup steps that the skill does not manage. <br>
Mitigation: Handle wallet credentials and node activation steps directly, and back up mnemonics outside the skill workflow. <br>


## Reference(s): <br>
- [Stratos SDS Resource Node Setup Guide](docs/setup-guide-en.md) <br>
- [Stratos SDS Resource Node Setup Guide (Chinese)](docs/setup-guide-zh.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/notboxqsn/stratos-storage) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Stratos file hashes or CIDs after successful uploads and local file paths after successful downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
