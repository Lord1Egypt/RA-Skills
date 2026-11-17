## Description:

Site Analyzing Tools analyzes a domain or IP address and produces a website and network profile covering hosting location, ISP and ASN attribution, DNS and GeoDNS behavior, WHOIS details, traceroute path, latency, and robots.txt policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfromdowntown](https://clawhub.ai/user/evanfromdowntown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to inspect domains or IP addresses for hosting attribution, DNS behavior, route quality, registration details, and crawler policy before troubleshooting, monitoring, or documenting a site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can actively probe third-party domains or IP addresses through DNS queries, WHOIS, traceroute, ping, TCP connection checks, and robots.txt fetches.

Mitigation: Use it only for targets you are authorized to analyze, and disable traceroute, ping, or robots checks when active probing is not appropriate.

Risk: The first-run environment probe profiles the user's own network and stores local exit IP, location, ISP, DNS, and tool availability data.

Mitigation: Review or disable the environment probe before managed-network use, and remove ~/.site-analyzer-env.json when the local profile should not be retained.

Risk: External lookup behavior includes plaintext HTTP requests and may send target IPs or domains to third-party services.

Mitigation: Avoid sensitive internal domains or customer IPs, and replace plaintext or untrusted lookup paths with approved HTTPS-only services before private-network deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evanfromdowntown/skills/site-analyze)
- [ip-api lookup endpoint](http://ip-api.com/json/{ip})
- [ipinfo lookup endpoint](https://ipinfo.io/{ip}/json)
- [api.ipify IP endpoint](https://api.ipify.org)
- [AliDNS DNS over HTTPS endpoint](https://dns.alidns.com/resolve)
- [Google DNS over HTTPS endpoint](https://dns.google/resolve)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text reports or JSON records with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local first-run network profile to ~/.site-analyzer-env.json.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
