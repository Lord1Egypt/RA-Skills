## Description: <br>
Monitors self-hosted services by checking HTTP endpoints, TCP ports, SSL certificate expiry, and DNS resolution, then reports status and alerts in concise, chat-friendly formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and self-hosted infrastructure maintainers use this skill to check whether configured HTTP, TCP, DNS, and TLS endpoints are healthy and to summarize alerts for agent-assisted monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill monitors endpoints and writes service inventory or outage history that may be sensitive. <br>
Mitigation: Use --no-history or configure a private history_file path when service names, endpoints, or outage records should not be persisted. <br>
Risk: HTTPS checks use curl with --insecure, which can mask certificate trust failures in normal endpoint checks. <br>
Mitigation: Review and remove the default --insecure behavior before relying on HTTPS health results for trusted production monitoring. <br>
Risk: TCP checks can fall back to bash /dev/tcp when nc or ncat is unavailable. <br>
Mitigation: Install nc or ncat and run the skill in an environment where monitored hosts and watchdog.json are trusted and controlled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mariusfit/service-watchdog) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Watchdog script](artifact/watchdog.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus summary, report, alerts-only, SSL-only, and JSON runtime output modes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local watchdog.json configuration and can append service status history to a CSV file unless run with --no-history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/watchdog.sh) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
