## Description:

Documents the session routing layer and authsession service in Teamgram Server, covering auth_key aggregation, IDMap routing, MainAuthWrapper, and backpressure mechanisms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as reference guidance for understanding Teamgram Server session routing, auth key/session management, authsession state, and related configuration points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration snippets may be copied into a real deployment without review.

Mitigation: Review and adapt the Teamgram MySQL, Redis, Etcd, and localhost listener settings before applying them outside the default development setup.

Risk: Reference guidance may become stale as Teamgram Server evolves.

Mitigation: Compare the described session routing, authsession behavior, and code paths against the current Teamgram Server source before making production changes.

## Reference(s):

- [Teamgram Server Repository](https://github.com/teamgram/teamgram-server)
- [ClawHub Skill Page](https://clawhub.ai/zhihang9978/skills/teamgram-session-layer)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown reference guidance with YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code, network calls, credential handling, or requested system access.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
