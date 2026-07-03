## Description: <br>
Checks the machine's public IP address, compares it with a local cache, reports whether it changed, and supports manual or scheduled runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xp1001](https://clawhub.ai/user/xp1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to check the current public IP address or monitor IP changes for scheduled tasks, DNS updates, and firewall allowlist maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public IP-check services. <br>
Mitigation: Install and schedule it only when those network requests are acceptable for the environment. <br>
Risk: The skill stores the last observed public IP address in ~/.public_ip_cache.json. <br>
Mitigation: Treat the cache as local operational data and remove it when IP history should not be retained. <br>
Risk: Scheduled automation could run the check more often than intended. <br>
Mitigation: Keep any schedule explicit and avoid triggering the skill from vague network-status comments unless that behavior is intended. <br>


## Reference(s): <br>
- [ip.sb public IP service](https://ip.sb) <br>
- [ipinfo.io IP endpoint](https://ipinfo.io/ip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown or plain text response with inline shell commands when execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make outbound HTTPS requests to public IP-check services and read or update ~/.public_ip_cache.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
