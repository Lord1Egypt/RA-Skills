## Description:

Proxq queues HTTP requests for asynchronous delivery to configured upstreams, then lets callers poll job status and retrieve responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Proxq to queue requests to trusted backends when callers need a quick response, then poll for completion and fetch the upstream result. It is suited to deferred API work and webhook delivery where real-time streaming is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because setup uses an unpinned Docker image and includes commands beyond the declared shell permissions; scan coverage is partial.

Mitigation: Review the flagged concerns and incomplete scan before installing, verify setup commands, and pin the Docker image to a trusted version.

Risk: The documented service has no built-in authentication and can make outbound requests to configured upstreams, so exposed instances can be misused to submit, inspect, or cancel jobs and reach unintended services.

Mitigation: Restrict access with an authentication proxy or an internal-only network, and configure only trusted upstreams that untrusted callers cannot select.

## Reference(s):

- [Setup and configuration guide](references/setup.md)
- [Project homepage](https://github.com/psyb0t/docker-proxq)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/proxq)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, HTTP API calls, Guidance]

**Output Format:** [Markdown with shell commands, YAML examples, and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Proxq instance and reachable Redis service; examples use PROXQ_URL.]

## Skill Version(s):

0.11.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
