## Description:

Set up and analyze shadow traffic testing to compare new service versions against production without user impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to configure traffic mirroring and compare production and shadow service behavior before promoting a new service version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mirroring full production requests can expose credentials, cookies, or sensitive request data to the shadow service.

Mitigation: Use only with approval from service, security, and privacy stakeholders; restrict mirrored routes, sample traffic, and strip credentials and cookies before requests reach the shadow service.

Risk: A cloned shadow deployment can inherit production-level privileges and dependencies.

Mitigation: Isolate the shadow service with separate low-privilege credentials and read-only dependencies.

Risk: Captured production and shadow logs may contain sensitive data if written to shared temporary files.

Mitigation: Avoid storing raw production logs in shared temporary files and apply approved retention and access controls to any collected logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Kubernetes YAML, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance, verification steps, analysis snippets, and report templates for shadow traffic testing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
