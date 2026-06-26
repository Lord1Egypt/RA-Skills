## Description: <br>
Upload, manage, retrieve, and check files on IPFS through Storacha decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adielliot37](https://clawhub.ai/user/adielliot37) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a Storacha CLI account from an agent: uploading files or directories, retrieving gateway links, checking usage, managing spaces, and handling delegations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files are publicly accessible through IPFS gateway links and may be difficult to fully retract. <br>
Mitigation: Confirm uploads before execution, avoid unencrypted sensitive data, and treat generated CIDs and gateway links as public. <br>
Risk: The skill can operate a Storacha CLI account, including changing spaces, deleting listings, and creating delegations. <br>
Mitigation: Confirm account-changing actions such as uploads, deletions, space changes, and delegations before running the corresponding commands. <br>
Risk: Storage usage, provider registration, or authentication issues can cause operations to fail or produce incomplete status results. <br>
Mitigation: Run the health-check flow before important uploads and verify authentication, active space, provider registration, and available storage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adielliot37/storacha-upload) <br>
- [Storacha Documentation](https://docs.storacha.network) <br>
- [Storacha Console](https://console.storacha.network) <br>
- [Storacha CLI Reference](https://github.com/storacha/storacha/tree/main/packages/cli) <br>
- [IPFS Gateway](https://storacha.link) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and gateway links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Storacha CIDs, public gateway URLs, account status summaries, and CLI setup guidance.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
