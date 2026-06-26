## Description: <br>
A high-performance Telegram Cloud Storage solution using Teldrive. Turns Telegram into an unlimited cloud drive with a local API/UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oki3505F](https://clawhub.ai/user/oki3505F) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure and operate a local Teldrive service that exposes Telegram-backed cloud storage through a web UI, REST API, and Python client commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation script downloads and runs an external Teldrive binary. <br>
Mitigation: Install only when the upstream Teldrive release source is trusted, and review the downloaded binary before deployment in sensitive environments. <br>
Risk: The skill handles Telegram API credentials, JWT tokens, session hashes, and database session data. <br>
Mitigation: Protect config.toml, token.txt, TELDRIVE_TOKEN, TELDRIVE_SESSION_HASH, and database session rows as credentials; restrict file permissions and do not commit or share them. <br>
Risk: Agent commands can upload, rename, delete, or download storage objects. <br>
Mitigation: Require explicit approval before file-changing operations and stop the background Teldrive process when it is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oki3505F/telegram-cloud-storage) <br>
- [Teldrive project](https://github.com/tgdrive/teldrive) <br>
- [Teldrive upstream author profile](https://github.com/divyam234) <br>
- [Telegram API portal](https://my.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands, configuration values, and JSON output from client operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Teldrive service at http://localhost:8080/api and may create local config, token, pid, log, and downloaded/uploaded files.] <br>

## Skill Version(s): <br>
1.8.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
