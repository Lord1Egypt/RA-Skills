## Description:

Checks the machine's public IP, reports whether it changed compared with a local cache, and updates the cache after each run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xp1001](https://clawhub.ai/user/xp1001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to check the current public IP address and notice changes that may affect DNS records, firewall allowlists, or other IP-dependent services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a request to an external public IP service, exposing that the local environment queried its public IP.

Mitigation: Run it only in environments where querying ip.sb or ipinfo.io is acceptable, and review the endpoint choice before scheduled use.

Risk: The skill stores the latest public IP address and timestamp in a local cache file.

Mitigation: Treat ~/.public_ip_cache.json as local operational data and remove it when the history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xp1001/skills/public-ip-watch)
- [ip.sb public IP endpoint](https://ip.sb)
- [ipinfo.io IP endpoint](https://ipinfo.io/ip)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown response with shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON cache at ~/.public_ip_cache.json and queries ip.sb or ipinfo.io to determine the current public IP.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
