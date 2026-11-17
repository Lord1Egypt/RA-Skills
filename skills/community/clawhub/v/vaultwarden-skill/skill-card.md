## Description:

Manage Vaultwarden secrets with wrapper scripts for session handling, caching, logging, and scoped read/write operations in collections or personal vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate to Vaultwarden through the Bitwarden CLI, then list, read, create, update, delete, and rotate vault items while preserving session state and operational logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate beyond the advertised collection scope and may access or mutate every item available to the authenticated Bitwarden account.

Mitigation: Install only when the agent is allowed to access and mutate the full authenticated vault, and avoid broad vault credentials until collection-membership checks are added.

Risk: Sensitive session tokens and cached credential material may be stored on disk.

Mitigation: Keep VW_SESSION_DIR private, lock the vault when done, and prefer disabling the read cache with VW_CACHE_TTL=0.

Risk: A wrong or unexpected Bitwarden server configuration could direct authentication or vault operations to the wrong service.

Mitigation: Manually verify the Bitwarden server configuration before unlocking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbojer/skills/vaultwarden-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command usage and script-generated text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shell scripts may read secrets from stdin, write status to stderr, and emit secret values or item JSON on stdout for selected read and rotation operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
