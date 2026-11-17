## Description:

Install, start, stop, and health-check Yuzhua (gesture + voice + OpenClaw gateway) with minimal manual setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juguangyuan520-dotcom](https://clawhub.ai/user/juguangyuan520-dotcom)

### License/Terms of Use:


## Use Case:

Developers and local OpenClaw users use this skill to install, run, stop, and health-check Yuzhua, a local gesture and voice chat app connected through the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and start flow can download and run mutable external code from the configured Yuzhua repository.

Mitigation: Install only trusted upstream code; review YUZHUA_REPO_URL and YUZHUA_HOME before use, and pin or audit the checkout for sensitive deployments.

Risk: The stop command can terminate any process listening on the configured port, including unrelated services on the default port 8080.

Mitigation: Verify YUZHUA_PORT and active listeners before running stop.sh, especially on machines running other local services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juguangyuan520-dotcom/skills/yuzhua)
- [Yuzhua Project Repository](https://github.com/juguangyuan520-dotcom/Yuzhua)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local Yuzhua checkout and .env file; health checks can print JSON from the local status endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
