## Description: <br>
Staking is a command-line skill that records, lists, searches, removes, exports, and reports statistics for local plaintext entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill as a simple local note tracker for staking-related notes and status records. It should not be relied on for staking operations, on-chain analysis, or protocol-security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims to analyze staking operations and protocol security, but the security summary identifies the implementation as a local plaintext entry tracker. <br>
Mitigation: Use it only for local notes and records; verify staking, on-chain, and protocol-security conclusions with separate trusted tools and human review. <br>
Risk: Entries and exported files may contain sensitive wallet, credential, or operational data in plaintext. <br>
Mitigation: Do not store private keys, seed phrases, wallet credentials, or sensitive operational data, and review ~/.staking plus staking-export files after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/staking) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text command output with optional JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses STAKING_DIR to choose the local data directory; defaults to ~/.staking/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
