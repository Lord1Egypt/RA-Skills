## Description:

Measure internet network speed, including download, upload, and ping, using speedtest-cli for Speedtest.net.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elony-7](https://clawhub.ai/user/elony-7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill to run a host network speed test and report ping, download, and upload results. It is useful when a user asks to check bandwidth, test internet speed, or diagnose connection performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the test contacts external Speedtest servers and may expose IP, ISP, and server information in JSON output.

Mitigation: Run only when the user accepts the network and privacy implications, and avoid sharing JSON output where IP or ISP details should remain private.

Risk: Unpinned speedtest-cli installations can vary across package managers and versions.

Mitigation: Install speedtest-cli manually in an isolated, unprivileged environment and pin the package version when reproducible behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elony-7/skills/speedtest-net)
- [Publisher profile](https://clawhub.ai/user/elony-7)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON speed test results with setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Speedtest server details, ISP, and IP address when JSON output is requested.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
