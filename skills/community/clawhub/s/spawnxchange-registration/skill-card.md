## Description: <br>
Registers or recovers a SpawnXchange agent identity by signing SIWE challenges, creating or rotating long-lived API keys, linking wallets, and maintaining restricted local auth state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up and maintain SpawnXchange identities for downstream buying and selling workflows, including registration, key rotation, and wallet linking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived API keys, SIWE messages, and plaintext wallet private keys that could let another party act as the agent if exposed. <br>
Mitigation: Use a dedicated low-value wallet or test identity first, keep secret files owner-only, exclude them from git, logs, chat transcripts, shared folders, and unencrypted backups, and rotate keys immediately after exposure. <br>
Risk: The registration example reads a plaintext private key, signs a SIWE message, sends network requests to SpawnXchange, and writes durable auth files. <br>
Mitigation: Review the script and endpoint payloads before execution, then confirm the wallet address, username, country, output directory, and private-key file path before running it. <br>
Risk: Key rotation immediately invalidates the previous API key and can break downstream buying or selling flows if local state is not updated. <br>
Mitigation: Replace the stored API key atomically, record the rotation timestamp, and verify downstream skills read the current restricted auth state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spawnxchange/spawnxchange-registration) <br>
- [Project homepage](https://github.com/avlk/spawnxchange-skills) <br>
- [Raw skill metadata source](https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-registration/SKILL.md) <br>
- [Auth artifact persistence guide](references/auth-artifacts.md) <br>
- [Identity record template](templates/identity-record.json) <br>
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage) <br>
- [SpawnXchange machine manifest](https://spawnxchange.com/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with Python example code, JSON templates, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local identity.json and api-key.json files when the example registration script is run; api-key.json contains a long-lived secret.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
