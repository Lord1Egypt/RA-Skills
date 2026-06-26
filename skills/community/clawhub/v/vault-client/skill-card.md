## Description: <br>
Hashicorp Vault client for OpenClaw agents that reads and writes Vault secrets, checks token expiry, rotates tokens, and helps configure Vault access without raw curl commands or hardcoded tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbushman](https://clawhub.ai/user/jbushman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents to Hashicorp Vault for reading, writing, listing, caching, and rotating secrets during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault tokens and cached secrets are stored in plaintext files under ~/.openclaw. <br>
Mitigation: Use least-privileged, short-lived Vault tokens and protect or remove ~/.openclaw/vault.json and ~/.openclaw/vault-cache.json after use. <br>
Risk: Setup can add persistent instructions to AGENTS.md. <br>
Mitigation: Inspect the AGENTS.md block added by setup before relying on it in future agent sessions. <br>
Risk: Disabling TLS verification can weaken protection for Vault traffic. <br>
Mitigation: Keep tls.verify enabled except in controlled internal environments with an explicit need for self-signed certificates. <br>
Risk: The put command can modify Vault secrets. <br>
Mitigation: Review target paths and key-value pairs before running write operations. <br>


## Reference(s): <br>
- [Vault Auth Methods](references/auth-methods.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Vault CLI setup, check, get, put, list, token-info, and token-renew commands for agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
