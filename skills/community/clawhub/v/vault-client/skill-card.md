## Description:

Hashicorp Vault client for OpenClaw agents that reads and writes secrets from a Vault server without raw curl commands or hardcoded tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbushman](https://clawhub.ai/user/jbushman)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to let OpenClaw agents check Vault connectivity, read and write Vault secrets, list paths, inspect token status, renew tokens, and configure Vault access without hardcoding credentials in transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault credentials and cached secrets are persisted in local configuration and cache files.

Mitigation: Use least-privilege, short-lived Vault tokens; treat ~/.openclaw/vault.json and ~/.openclaw/vault-cache.json as sensitive files; and clear the cache when the session is done.

Risk: Disabling TLS verification or using an HTTP Vault address can expose secret traffic to interception.

Mitigation: Require HTTPS with a valid certificate, avoid tls.verify:false except for reviewed internal cases, and do not use http:// Vault addresses.

Risk: The setup flow can append Vault instructions to AGENTS.md, affecting future agent sessions.

Mitigation: Inspect AGENTS.md changes before allowing them to influence future sessions.

## Reference(s):

- [Vault Auth Methods](references/auth-methods.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, command-line output, and Markdown instructions with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, write, list, and cache Vault secret data depending on the command and configured Vault permissions.]

## Skill Version(s):

1.0.0 (source: release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
