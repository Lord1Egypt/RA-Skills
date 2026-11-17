## Description:

Wakehook helps an agent install, configure, authorize, and run a self-hosted wake-trigger service that converts Google Health/Fitbit sleep data into a neutral user.awake webhook for OpenClaw or Hermes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbeverhelst](https://clawhub.ai/user/robbeverhelst)

### License/Terms of Use:

MIT

## Use Case:

Developers and advanced users use Wakehook to connect sleep-derived wake signals to an agent or automation endpoint so morning routines can run when the user actually wakes up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wakehook handles sensitive sleep data and stores long-lived Google OAuth refresh tokens.

Mitigation: Protect or encrypt the SQLite database, keep OAuth credentials out of configuration files, and run the service only on trusted hosts.

Risk: An unset webhook token can leave inbound webhook behavior or test replay paths exposed during deployment.

Mitigation: Set strong webhook and admin tokens, disable or protect /test/replay, and bind the service to trusted interfaces.

Risk: Subscriber fan-out can send wake events to external endpoints.

Mitigation: Send events only to trusted HTTPS endpoints and use per-subscriber authentication or HMAC signatures.

Risk: The webhook mode requires public HTTPS exposure and is less verified than poll mode in the artifact documentation.

Mitigation: Prefer poll mode unless instant delivery is required, and test public webhook deployments before relying on them.

## Reference(s):

- [Wakehook ClawHub Skill Page](https://clawhub.ai/robbeverhelst/skills/wakehook)
- [Wakehook Project Homepage](https://github.com/robbeverhelst/wakehook)
- [Wakehook npm Package](https://www.npmjs.com/package/wakehook)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup choices for OpenClaw or Hermes, Google Health polling or webhook mode, OAuth authorization, and wake-event verification.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
