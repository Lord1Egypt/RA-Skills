## Description: <br>
Advertised for blockchain slashing analysis, but release security evidence says the included behavior is a local persistent entry and configuration manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users may use this skill to run a local note and configuration workflow with status, add, list, search, remove, export, stats, and config commands. It should not be treated as a blockchain slashing-analysis skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release description may lead users to expect blockchain slashing analysis, while the security evidence identifies local note and configuration management behavior. <br>
Mitigation: Review the artifact before installing and treat it as a local entry manager rather than a blockchain analysis tool. <br>
Risk: The remove, export, and config commands can mutate or copy local files. <br>
Mitigation: Use those commands only with explicit intent and test with a dedicated SLASHING_DIR before using persistent data. <br>
Risk: User-entered entries are persisted locally and could contain sensitive information. <br>
Mitigation: Avoid storing secrets, credentials, private keys, or sensitive operational data in the skill's local data files. <br>


## Reference(s): <br>
- [Slashing on ClawHub](https://clawhub.ai/bytesagain3/slashing) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, mutate, remove, or export local files under SLASHING_DIR or the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
