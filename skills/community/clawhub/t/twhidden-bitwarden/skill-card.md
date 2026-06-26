## Description: <br>
Bitwarden & Vaultwarden password manager integration. Use when storing, retrieving, generating, or managing passwords and credentials. Wraps the Bitwarden CLI (bw) with automatic session management. Works with both official Bitwarden and self-hosted Vaultwarden servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TWhidden](https://clawhub.ai/user/TWhidden) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw agent authenticate to a configured Bitwarden or Vaultwarden account, then retrieve, create, edit, delete, and generate credentials through the Bitwarden CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read, create, edit, delete, and register vault credentials through the configured Bitwarden/Vaultwarden account. <br>
Mitigation: Use a dedicated limited vault account and require explicit approval for read, create, edit, delete, and register actions. <br>
Risk: The skill depends on BW_SERVER, BW_EMAIL, and BW_MASTER_PASSWORD being available through environment variables or a credentials file. <br>
Mitigation: Avoid shared or backed-up plaintext credential files, keep credential files out of version control, and restrict file permissions. <br>
Risk: Session tokens are cached locally for subsequent commands. <br>
Mitigation: Run lock or logout when finished and avoid using the skill on shared machines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TWhidden/twhidden-bitwarden) <br>
- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/) <br>
- [Bitwarden](https://bitwarden.com/) <br>
- [Vaultwarden](https://github.com/dani-garcia/vaultwarden) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and Bitwarden CLI JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return decrypted credential values when vault read commands are used.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact _meta.json; changelog v1.0.5 dated 2026-02-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
