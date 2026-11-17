## Description:

Monitors self-hosted services by checking HTTP endpoints, TCP ports, SSL certificate expiry, and DNS resolution, then reports service status and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to check whether self-hosted services are healthy, review recent monitoring history, and surface alerts for outages, slow responses, DNS issues, or expiring TLS certificates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe configuration handling could let a bad config run commands or damage writable files.

Mitigation: Use only trusted watchdog.json files, avoid untrusted host, port, URL, and history_file values, prefer disabling history or confining it to a dedicated directory, and do not rely on HTTPS results for certificate trust until the insecure TLS behavior is corrected.

## Reference(s):

- [Service Watchdog on ClawHub](https://clawhub.ai/mariusfit/skills/service-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, status summaries, reports, and optional machine-readable JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit summary, detailed report, JSON, SSL-only, or alerts-only output depending on command flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
