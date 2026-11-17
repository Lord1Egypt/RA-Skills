## Description:

Access WHOOP fitness tracker data via API, including recovery scores, sleep metrics, workout stats, daily strain, and body measurements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijaack](https://clawhub.ai/user/ijaack)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve and summarize a user's WHOOP recovery, sleep, workout, daily strain, profile, and body-measurement data after OAuth authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read WHOOP health, workout, sleep, recovery, profile, and body-measurement data after authorization.

Mitigation: Install and authorize it only when this data access is acceptable, and grant only the WHOOP scopes needed for the intended task.

Risk: OAuth client credentials and tokens are stored locally under ~/.whoop.

Mitigation: Keep ~/.whoop/credentials.json and ~/.whoop/token.json private, avoid shared machines, use restrictive file permissions, and revoke tokens if they are exposed.

Risk: The install script installs the requests dependency with pip.

Mitigation: Use a virtual environment and pinned dependency versions when installing in managed or production environments.

## Reference(s):

- [WHOOP OAuth Setup](references/oauth.md)
- [WHOOP API Reference](references/api-reference.md)
- [WHOOP Developer Portal](https://developer.whoop.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOOP OAuth credentials and read scopes for profile, body measurement, recovery, sleep, cycles, and workout data.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
