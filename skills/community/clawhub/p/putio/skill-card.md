## Description: <br>
Manage a put.io account via the kaput CLI for transfers, files, search, and transfer status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baanish](https://clawhub.ai/user/baanish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and put.io users use this skill to install and operate the unofficial kaput CLI, authenticate with put.io, add transfers, list transfers, search files, and check account or transfer status from an agent-assisted shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unofficial kaput CLI stores a local put.io token and command output may expose account details. <br>
Mitigation: Use the documented device-code login, do not paste credentials or tokens into chat, avoid sharing debug output, and show account details only when intentionally requested. <br>
Risk: Transfer commands can add magnet links, torrent URLs, or direct URLs to a real put.io account. <br>
Mitigation: Review each transfer URL before execution and only add transfers the user intentionally wants in their account. <br>
Risk: The skill depends on an external kaput binary installed through Rust and Cargo. <br>
Mitigation: Install kaput-cli from a trusted source and set KAPUT_BIN only to the intended executable path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baanish/putio) <br>
- [Publisher profile](https://clawhub.ai/user/baanish) <br>
- [put.io device-code login](https://put.io/link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces shell-oriented guidance for an installed kaput CLI; command output may include put.io account, transfer, or file metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
