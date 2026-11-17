## Description:

Ravi Vault helps agents store and retrieve key-value secrets for API keys, environment variables, and tokens through an end-to-end encrypted CLI vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:


## Use Case:

Developers and external agents use Ravi Vault as a runtime backing store for API keys, environment variables, and service tokens. It is intended for key-value secrets, not website passwords or message retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets placed directly in shell commands or process arguments can leak through shell history, process listings, traces, or agent logs.

Mitigation: Prefer stdin or no-echo prompts when supported, disable shell tracing around secret handling, and keep agent/tool logs from recording decrypted values.

Risk: Retrieved secret values are shown to the agent in plaintext and can be exposed if subsequent commands or outputs are logged.

Mitigation: Limit retrieval to the moment of use, avoid printing decrypted values, and redact or suppress command output that may include credentials.

Risk: Secret keys are stored in plaintext for lookup and filtering.

Mitigation: Use descriptive non-sensitive key names and avoid embedding secret material or private account details in key names.

## Reference(s):

- [Ravi Vault ClawHub Skill Page](https://clawhub.ai/raunaksingwi/skills/ravi-vault)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret list output redacts values; retrieval output can include plaintext secret values.]

## Skill Version(s):

1.6.0 (source: server release metadata, released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
