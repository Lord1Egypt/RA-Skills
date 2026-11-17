## Description:

Report system issues and submit resource, access, configuration, service, deployment, and information requests to SysClaw through a cross-agent communication system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to report operational issues, submit resource or access requests, and check SysClaw responses through database-backed helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent notification polling can expose stored database credentials and repeatedly import external notification text.

Mitigation: Prefer manual notification checks, store credentials in a protected secret store or 0600 credential file, and avoid writing notifications directly into agent memory.

Risk: Notification contents and SysClaw responses are external data that may influence an agent session.

Mitigation: Treat notification text as untrusted data, verify requested actions against trusted SysClaw context, and use least-privileged database roles.

Risk: The helper scripts depend on psycopg2-binary and a reachable SysClaw database.

Mitigation: Pin the Python dependency, use trusted package sources, and install only where the SysClaw operator and database are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbojer/skills/sysclaw-reporting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, SQL, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts require Python 3, psycopg2-binary, and SysClaw database connection settings.]

## Skill Version(s):

4.0.0 (source: server release evidence and changelog, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
