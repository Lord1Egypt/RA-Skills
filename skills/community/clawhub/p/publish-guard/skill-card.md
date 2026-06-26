## Description: <br>
PublishGuard helps agents verify that published content is reachable, check platform-specific posting requirements, track rate limits, audit attempts, and manage publishing credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill when publishing to platforms such as BotMadang, Moltbook, and ClawHub to avoid false success reports, validate platform requirements, and preserve publishing state across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing tokens may be stored in plaintext by the default credential store despite encrypted-vault claims elsewhere in the artifact. <br>
Mitigation: Disable or replace the plaintext CredentialStore before storing real secrets, use the encrypted vault deliberately, and delete any publish_guard_creds.json files after testing. <br>
Risk: Stored publishing credentials could authorize real posts or account actions if exposed from a shared or backed-up workspace. <br>
Mitigation: Use low-privilege, revocable tokens and avoid storing production credentials in shared, synced, or long-lived workspaces. <br>


## Reference(s): <br>
- [PublishGuard ClawHub release page](https://clawhub.ai/edmonddantesj/publish-guard) <br>
- [Publisher profile](https://clawhub.ai/user/edmonddantesj) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Post verification engine](artifact/scripts/publish_guard.py) <br>
- [Credential vault implementation](artifact/scripts/vault_crypto.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python API results, shell command examples, and JSONL audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces platform-specific guidance, content validation results, post verification diagnoses, credential storage operations, and audit entries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
