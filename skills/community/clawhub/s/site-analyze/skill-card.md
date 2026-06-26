## Description: <br>
Analyzes domains and IP addresses to produce a site profile covering DNS resolution, IP ownership, ISP/ASN, traceroute path, latency, WHOIS registration, and robots.txt policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvanFromDowntown](https://clawhub.ai/user/EvanFromDowntown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and network engineers use this skill to inspect a domain or IP address and summarize hosting location, network path, ownership, connectivity, and crawling policy. It is intended for authorized analysis of public or user-controlled targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may disclose analyzed domains, IPs, route data, or DNS queries to third-party DNS and IP-information services. <br>
Mitigation: Use it only for targets you are authorized to test, notify users before remote lookups, and provide a no-remote-lookups mode for sensitive environments. <br>
Risk: The environment probe stores local network details in ~/.site-analyzer-env.json. <br>
Mitigation: Inspect or delete the file after use, and avoid running the probe on corporate, sensitive, or internal networks unless approved. <br>
Risk: Network-derived probe data may be handled unsafely if serialized into generated code or shell contexts. <br>
Mitigation: Serialize probe data with structured JSON writers and avoid embedding raw network-derived strings into executable code. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/EvanFromDowntown/site-analyze) <br>
- [ip-api JSON endpoint](http://ip-api.com/json/{ip}) <br>
- [ipinfo JSON endpoint](https://ipinfo.io/{ip}/json) <br>
- [Google DNS over HTTPS endpoint](https://dns.google/resolve) <br>
- [AliDNS DNS over HTTPS endpoint](https://dns.alidns.com/resolve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown or terminal text with optional JSON output from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run DNS, WHOIS, ping, traceroute, robots.txt, and IP information probes for a supplied domain or IP address.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
